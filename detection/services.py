"""
Service module for disease detection.

Pipeline (per product requirements):
  Stage 1  EfficientNet-B0     → Crop classification (Mango / Onion / Sugarcane)
  Stage 2  YOLOv8s-cls         → Disease detection  (per-crop disease class)
  Stage 3  RAG + OpenAI        → Recommendation generation (recommendation/rag.py)

After a successful scan:
  • A Prediction row is created.
  • A PredictionHistory row is created automatically.
  • A Recommendation row is created and RAG content is pre-generated so the
    recommendations page loads instantly (no waiting for the LLM on first view).
"""
import logging
import time
from pathlib import Path
from typing import Any, Dict, Optional

from django.conf import settings
from django.core.files.base import ContentFile

from .models import Crop, Disease, Prediction, ScanImage

logger = logging.getLogger("pakagri.detection")


# ─────────────────────────────────────────────────────────────────────────────
#  Internal service classes
# ─────────────────────────────────────────────────────────────────────────────

class CropClassifier:
    """EfficientNet-B0 crop classifier — Stage 1."""

    def classify(self, image_path: str):
        from .ml.inference import predict_crop
        return predict_crop(image_path)


class DiseasePredictor:
    """YOLOv8s-cls disease detector — Stage 2."""

    def predict_detailed(self, image_path: str, crop_name: str) -> Dict[str, Any]:
        from .ml.inference import predict_disease
        return predict_disease(image_path, crop_name)


class RecommendationEngine:
    """
    Lightweight KB-only recommendation summary used on the result page.
    The full bilingual, RAG-generated advice lives in recommendation/rag.py
    and is shown on the dedicated recommendations page.
    This stays a simple, dependency-free fallback so the result page
    never needs the LLM to render.
    """

    @staticmethod
    def get_recommendations(prediction: Prediction) -> Dict[str, Any]:
        recommendations = {"treatment": [], "prevention": [], "urgency": "normal"}

        if prediction.disease:
            recommendations["treatment"] = [
                line for line in prediction.disease.treatment.split("\n") if line.strip()
            ] or ["See the Recommendations page for detailed treatment guidance."]
            recommendations["prevention"] = [
                line for line in prediction.disease.prevention.split("\n") if line.strip()
            ] or ["See the Recommendations page for prevention guidance."]

            if prediction.confidence_level == "high":
                recommendations["urgency"] = "urgent"
            elif prediction.confidence_level == "medium":
                recommendations["urgency"] = "moderate"
        else:
            recommendations["urgency"] = "none"
            recommendations["treatment"] = ["Continue regular crop maintenance."]
            recommendations["prevention"] = [
                "Maintain proper irrigation.",
                "Monitor plant health regularly.",
            ]

        return recommendations


# ─────────────────────────────────────────────────────────────────────────────
#  Main orchestrator
# ─────────────────────────────────────────────────────────────────────────────

class DetectionService:
    """
    Orchestrates the full scan pipeline:
      upload → classify crop → detect disease → save prediction
              → create history → pre-generate RAG recommendation
    """

    def __init__(self):
        self.crop_classifier = CropClassifier()
        self.disease_predictor = DiseasePredictor()
        self.recommendation_engine = RecommendationEngine()

    # ── helpers ──────────────────────────────────────────────────────────────

    def _resolve_disease(self, crop: Optional[Crop], raw_label: Optional[str]) -> Optional[Disease]:
        """
        Maps a model's raw output label back to its Disease row.
        Prefers exact `raw_class_name` match; falls back to case-insensitive name match.
        """
        if not raw_label or crop is None:
            return None
        disease = Disease.objects.filter(crop=crop, raw_class_name=raw_label).first()
        if disease is None:
            disease = Disease.objects.filter(crop=crop, name__iexact=raw_label).first()
        if disease is None:
            logger.warning(
                "No Disease row found for crop=%s raw_label=%s — "
                "run `python manage.py sync_ml_metadata` if this class is new.",
                crop.name, raw_label,
            )
        return disease

    def _save_analysis_image(self, prediction: Prediction, image_path: str,
                             crop_name: str, disease_result: Dict[str, Any]) -> None:
        """Attaches Grad-CAM heatmap (uses EfficientNet conv layers). Best-effort only."""
        from .ml.gradcam import generate_analysis_image
        from .ml.registry import get_registry

        if disease_result["is_healthy"] or not disease_result["disease_label"]:
            return

        registry = get_registry()
        model_set = registry.disease_models.get(crop_name)
        if model_set is None or not model_set.has_effnet:
            return

        try:
            class_idx = model_set.classes.index(disease_result["disease_label"])
        except ValueError:
            return

        tmp_output = Path(settings.MEDIA_ROOT) / "scans" / "analysis" / "_tmp_gradcam.jpg"
        tmp_output.parent.mkdir(parents=True, exist_ok=True)

        success = generate_analysis_image(
            image_path=image_path,
            effnet_model=model_set.effnet_model,
            class_idx=class_idx,
            label=disease_result["disease_label"],
            confidence=disease_result["confidence"],
            output_path=str(tmp_output),
        )
        if success:
            with open(tmp_output, "rb") as f:
                prediction.analysis_image.save(
                    f"gradcam_{prediction.id}.jpg", ContentFile(f.read()), save=True
                )
            tmp_output.unlink(missing_ok=True)

    @staticmethod
    def _create_history(prediction: Prediction) -> None:
        """Auto-creates a PredictionHistory row after every successful scan."""
        try:
            from history.models import PredictionHistory
            PredictionHistory.objects.get_or_create(
                prediction=prediction,
                defaults={"user": prediction.scan_image.user},
            )
            logger.debug("PredictionHistory created for prediction %s", prediction.id)
        except Exception:
            logger.exception("Failed to create PredictionHistory for prediction %s", prediction.id)

    @staticmethod
    def _pre_generate_rag(prediction: Prediction, disease: Optional[Disease]) -> None:
        """
        Stage 3 — Pre-generates the RAG recommendation so the recommendation page
        loads instantly. Runs in the same request (synchronous), but errors never
        block the result page from showing.
        """
        try:
            from recommendation.models import Recommendation
            from recommendation.rag import generate_recommendation

            recommendation, _ = Recommendation.objects.get_or_create(
                prediction=prediction,
                defaults={
                    "disease": disease,
                    "treatment_steps": disease.treatment if disease else "Continue regular monitoring.",
                    "prevention_steps": disease.prevention if disease else "Maintain proper irrigation.",
                    "urgency": "urgent" if prediction.confidence_level == "high" else "normal",
                },
            )
            # Generate and cache the bilingual RAG content
            generate_recommendation(recommendation)
            logger.info("RAG recommendation pre-generated for prediction %s", prediction.id)
        except Exception:
            logger.exception(
                "RAG pre-generation failed for prediction %s — "
                "will generate on first page view instead.", prediction.id
            )

    # ── main pipeline ─────────────────────────────────────────────────────────

    def process_scan(self, scan_image: ScanImage) -> Optional[Prediction]:
        """
        Full pipeline:
          1. EfficientNet-B0  → classify crop
          2. YOLOv8s-cls      → detect disease
          3. Save Prediction row
          4. Auto-create PredictionHistory
          5. Pre-generate RAG recommendation

        Returns None on any fatal failure (errors are logged; view shows user message).
        """
        try:
            start_time = time.time()
            image_path = scan_image.image.path
            logger.info("─── Scan %s started: %s ───", scan_image.id, image_path)

            # ── Stage 1: Crop Classification (EfficientNet-B0) ────────────────
            crop_name, crop_confidence = self.crop_classifier.classify(image_path)
            if not crop_name:
                logger.error(
                    "Scan %s — crop classifier returned no result. "
                    "Verify ML_MODELS_DIR=%s contains classification/effnet_b0_best.pth",
                    scan_image.id, getattr(settings, "ML_MODELS_DIR", "NOT SET"),
                )
                return None

            logger.info(
                "Scan %s — Stage 1 done: crop='%s' (%.1f%%)",
                scan_image.id, crop_name, crop_confidence * 100,
            )

            crop = Crop.objects.filter(name__iexact=crop_name).first()
            if not crop:
                logger.error(
                    "Scan %s — crop '%s' not in DB. Run: python manage.py sync_ml_metadata",
                    scan_image.id, crop_name,
                )
                return None

            # ── Stage 2: Disease Detection (YOLOv8s-cls) ──────────────────────
            disease_result = self.disease_predictor.predict_detailed(image_path, crop_name)

            logger.info(
                "Scan %s — Stage 2 done: label='%s' healthy=%s confidence=%.1f%%",
                scan_image.id,
                disease_result.get("disease_label", "N/A"),
                disease_result["is_healthy"],
                disease_result["confidence"] * 100,
            )

            disease = self._resolve_disease(crop, disease_result["disease_label"])

            # ── Confidence bucket ──────────────────────────────────────────────
            confidence = disease_result["confidence"]
            if confidence >= 0.8:
                confidence_level = "high"
            elif confidence >= 0.5:
                confidence_level = "medium"
            else:
                confidence_level = "low"

            processing_time = time.time() - start_time

            # ── Save Prediction ───────────────────────────────────────────────
            prediction = Prediction.objects.create(
                scan_image=scan_image,
                crop=crop,
                disease=disease,
                confidence_score=confidence,
                confidence_level=confidence_level,
                is_healthy=disease_result["is_healthy"],
                is_uncertain=False,                          # single model — no disagreement
                effnet_top_label="",                         # EfficientNet not used for disease
                effnet_top_confidence=0.0,
                yolo_top_label=disease_result["yolo_label"],
                yolo_top_confidence=disease_result["yolo_confidence"],
                processing_time=processing_time,
            )

            logger.info(
                "Scan %s — Prediction #%s saved in %.2fs (crop=%s, disease=%s)",
                scan_image.id, prediction.id, processing_time,
                crop_name, disease.name if disease else "Healthy",
            )

            # ── Grad-CAM visualisation (best-effort) ─────────────────────────
            try:
                self._save_analysis_image(prediction, image_path, crop_name, disease_result)
            except Exception:
                logger.exception("Grad-CAM step failed — continuing without it.")

            # ── Mark scan processed ───────────────────────────────────────────
            scan_image.is_processed = True
            scan_image.save()

            # ── Stage 3: History + RAG (after commit, non-blocking) ───────────
            self._create_history(prediction)
            self._pre_generate_rag(prediction, disease)

            logger.info("─── Scan %s complete ───", scan_image.id)
            return prediction

        except Exception:
            logger.exception("Error processing scan %s", getattr(scan_image, "id", "?"))
            return None

    def get_prediction_details(self, prediction: Prediction) -> Dict[str, Any]:
        recommendations = self.recommendation_engine.get_recommendations(prediction)

        return {
            "prediction_id": prediction.id,
            "crop": prediction.crop.name if prediction.crop else None,
            "disease": prediction.disease.name if prediction.disease else "Healthy Plant",
            "confidence_score": prediction.get_confidence_percentage(),
            "confidence_level": prediction.get_confidence_level_display(),
            "is_healthy": prediction.is_healthy,
            "is_uncertain": prediction.is_uncertain,
            "yolo_top_label": prediction.yolo_top_label,
            "yolo_top_confidence": round(prediction.yolo_top_confidence * 100, 1),
            "processing_time": round(prediction.processing_time, 2),
            "predicted_at": prediction.predicted_at.isoformat(),
            "disease_description": prediction.disease.description if prediction.disease else None,
            "symptoms": prediction.disease.symptoms if prediction.disease else None,
            "treatment": prediction.disease.treatment if prediction.disease else None,
            "prevention": prediction.disease.prevention if prediction.disease else None,
            "recommendations": recommendations,
        }


def get_detection_service() -> "DetectionService":
    """
    Factory used by views.py.
    Returns CrewAI pipeline if USE_CREWAI_PIPELINE=True, otherwise the direct pipeline.
    Both expose the same process_scan() / get_prediction_details() interface.
    """
    if getattr(settings, "USE_CREWAI_PIPELINE", False):
        from .crew_service import CrewDetectionService
        return CrewDetectionService()
    return DetectionService()
