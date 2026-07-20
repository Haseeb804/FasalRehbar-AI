"""
CrewAI tools. Each tool is a thin wrapper around already-existing, already-tested
code (detection/ml/inference.py and recommendation/rag.py) — the tools do not
contain any new ML or LLM-prompting logic themselves.
"""
from typing import Optional, Type

from pydantic import BaseModel, Field

from crewai.tools import BaseTool

from .schemas import CropClassificationOutput, DiseaseDetectionOutput, RecommendationOutput, LocalizedAdvice


class ClassifyCropInput(BaseModel):
    """Input schema for the crop classification tool."""
    image_path: str = Field(..., description="Absolute filesystem path to the uploaded crop image.")


class ClassifyCropTool(BaseTool):
    name: str = "classify_crop"
    description: str = (
        "Classifies which crop (Mango, Onion, or Sugarcane) appears in an image, using the "
        "EfficientNet-B0 crop classifier. Input is the absolute image_path. Returns the crop "
        "name and confidence score."
    )
    args_schema: Type[BaseModel] = ClassifyCropInput

    def _run(self, image_path: str) -> CropClassificationOutput:
        from detection.ml.inference import predict_crop

        crop_name, confidence = predict_crop(image_path)
        if not crop_name:
            # Tools should return informative results rather than raise, so the
            # agent can react (e.g. explain the failure) instead of crashing.
            return CropClassificationOutput(crop="Unknown", confidence=0.0)
        return CropClassificationOutput(crop=crop_name, confidence=confidence)


class DetectDiseaseInput(BaseModel):
    """Input schema for the disease detection tool."""
    image_path: str = Field(..., description="Absolute filesystem path to the uploaded crop image.")
    crop_name: str = Field(..., description="The crop name determined by the classification step (Mango/Onion/Sugarcane).")


class DetectDiseaseTool(BaseTool):
    name: str = "detect_disease"
    description: str = (
        "Detects plant disease for a given crop image, using an ensemble of EfficientNet-B0 and "
        "YOLOv8s-cls. Input is the absolute image_path and the crop_name from the classification "
        "step. Returns the disease label (or indicates healthy), confidence, and whether the two "
        "underlying models agreed on the diagnosis."
    )
    args_schema: Type[BaseModel] = DetectDiseaseInput

    def _run(self, image_path: str, crop_name: str) -> DiseaseDetectionOutput:
        from detection.ml.inference import predict_disease

        result = predict_disease(image_path, crop_name)
        return DiseaseDetectionOutput(
            disease_label=result["disease_label"],
            confidence=result["confidence"],
            is_healthy=result["is_healthy"],
            is_uncertain=result["is_uncertain"],
            effnet_label=result["effnet_label"],
            effnet_confidence=result["effnet_confidence"],
            yolo_label=result["yolo_label"],
            yolo_confidence=result["yolo_confidence"],
        )


class GenerateRecommendationInput(BaseModel):
    """Input schema for the recommendation generation tool."""
    crop_name: str = Field(..., description="The identified crop, e.g. 'Mango'.")
    disease_label: Optional[str] = Field(None, description="Raw disease class name, or null/omitted if the plant is healthy.")
    is_healthy: bool = Field(..., description="Whether the plant was diagnosed as healthy.")
    confidence: float = Field(..., description="Detection confidence, 0.0-1.0.")
    is_uncertain: bool = Field(False, description="True if EfficientNet and YOLOv8s-cls disagreed.")
    effnet_label: str = Field("", description="EfficientNet-B0's top prediction label.")
    effnet_confidence: float = Field(0.0, description="EfficientNet-B0's top confidence.")
    yolo_label: str = Field("", description="YOLOv8s-cls's top prediction label.")
    yolo_confidence: float = Field(0.0, description="YOLOv8s-cls's top confidence.")


class GenerateRecommendationTool(BaseTool):
    name: str = "generate_recommendation"
    description: str = (
        "Generates bilingual (English and Urdu) farmer-facing advice — summary, symptoms, causes, "
        "organic treatment, chemical treatment, prevention, severity, and when to consult a human "
        "expert — strictly grounded in the disease knowledge base. Input is the crop, disease "
        "(or healthy status), and confidence/agreement details from the detection step."
    )
    args_schema: Type[BaseModel] = GenerateRecommendationInput

    def _run(self, crop_name: str, is_healthy: bool, confidence: float, disease_label: Optional[str] = None,
              is_uncertain: bool = False, effnet_label: str = "", effnet_confidence: float = 0.0,
              yolo_label: str = "", yolo_confidence: float = 0.0) -> RecommendationOutput:
        from core.models import Crop, Disease
        from recommendation.rag import generate_content

        crop = Crop.objects.filter(name__iexact=crop_name).first()
        disease = None
        if not is_healthy and disease_label and crop:
            disease = Disease.objects.filter(crop=crop, raw_class_name=disease_label).first()
            if disease is None:
                disease = Disease.objects.filter(crop=crop, name__iexact=disease_label).first()

        context = {
            "crop_name": crop_name,
            "is_healthy": is_healthy,
            "confidence": confidence,
            "is_uncertain": is_uncertain,
            "effnet_label": effnet_label,
            "effnet_confidence": effnet_confidence,
            "yolo_label": yolo_label,
            "yolo_confidence": yolo_confidence,
            "knowledge_base": {
                "name": disease.name if disease else disease_label,
                "description": disease.description if disease else "",
                "symptoms": disease.symptoms if disease else "",
                "causes": disease.causes if disease else "",
                "treatment": disease.treatment if disease else "",
                "prevention": disease.prevention if disease else "",
                "severity": disease.get_severity_display() if disease else "",
            },
        }

        content = generate_content(context)
        return RecommendationOutput(
            en=LocalizedAdvice(**content.get("en", {})),
            ur=LocalizedAdvice(**content.get("ur", {})),
        )
