"""
CrewAI-orchestrated alternative to DetectionService.

Same external interface (process_scan, get_prediction_details — the latter is
inherited unchanged) so views.py doesn't need to know which pipeline is active.
Enable with USE_CREWAI_PIPELINE=True in .env.

IMPORTANT TRADEOFF: this adds a full LLM reasoning pass (3 agent turns) around
every scan purely for orchestration - the underlying computation (the actual
crop/disease models, the RAG grounding) is byte-for-byte the same code the
direct DetectionService pipeline calls. That means: extra latency (LLM round
trips on top of model inference), extra cost (OpenAI calls per scan, not just
per recommendation), and an extra failure surface (a confused agent could call
a tool with the wrong argument). For a deterministic pipeline like this one,
the direct DetectionService is the recommended default; this exists for cases
where you want CrewAI's structure/observability or plan to extend the agents
with more autonomous behavior later (e.g. an agent deciding whether to escalate
a case to a human expert).
"""
import logging
import time

from django.utils import timezone

from .models import Crop, Prediction, ScanImage
from .services import DetectionService

logger = logging.getLogger("pakagri.crew")


class CrewDetectionService(DetectionService):

    def process_scan(self, scan_image: ScanImage):
        from recommendation.models import Recommendation
        from .crew.pipeline import run_pipeline

        try:
            start_time = time.time()
            image_path = scan_image.image.path

            outputs = run_pipeline(image_path)
            classification = outputs["classification"]
            detection = outputs["detection"]
            recommendation_output = outputs["recommendation"]

            crop = Crop.objects.filter(name__iexact=classification.crop).first()
            if not crop:
                logger.error("Crew pipeline: crop '%s' not found in database.", classification.crop)
                return None

            disease = self._resolve_disease(crop, detection.disease_label)

            confidence = detection.confidence
            if confidence >= 0.8:
                confidence_level = "high"
            elif confidence >= 0.5:
                confidence_level = "medium"
            else:
                confidence_level = "low"

            processing_time = time.time() - start_time

            prediction = Prediction.objects.create(
                scan_image=scan_image,
                crop=crop,
                disease=disease,
                confidence_score=confidence,
                confidence_level=confidence_level,
                is_healthy=detection.is_healthy,
                is_uncertain=detection.is_uncertain,
                effnet_top_label=detection.effnet_label,
                effnet_top_confidence=detection.effnet_confidence,
                yolo_top_label=detection.yolo_label,
                yolo_top_confidence=detection.yolo_confidence,
                processing_time=processing_time,
                model_version="crewai-v1.0",
            )

            # Grad-CAM visualization (best-effort; never blocks the result)
            try:
                self._save_analysis_image(prediction, image_path, classification.crop, {
                    "is_healthy": detection.is_healthy,
                    "disease_label": detection.disease_label,
                    "confidence": detection.confidence,
                })
            except Exception:
                logger.exception("Grad-CAM step failed in crew pipeline; continuing without it.")

            # The recommendation agent already produced bilingual advice via the
            # same underlying generate_content() the direct pipeline uses -
            # cache it directly rather than calling the RAG engine a second time.
            is_urgent = bool(disease) and confidence_level == "high" and not detection.is_uncertain
            Recommendation.objects.update_or_create(
                prediction=prediction,
                defaults={
                    "disease": disease,
                    "treatment_steps": disease.treatment if disease else "Keep plant healthy",
                    "prevention_steps": disease.prevention if disease else "Monitor regularly",
                    "urgency": "urgent" if is_urgent else ("moderate" if detection.is_uncertain else "normal"),
                    "ai_content": {
                        "en": recommendation_output.en.model_dump(),
                        "ur": recommendation_output.ur.model_dump(),
                    },
                    "ai_content_generated_at": timezone.now(),
                    "ai_generation_error": "",
                },
            )

            scan_image.is_processed = True
            scan_image.save()

            return prediction

        except Exception:
            logger.exception("CrewAI pipeline failed for scan %s", getattr(scan_image, "id", "?"))
            return None
