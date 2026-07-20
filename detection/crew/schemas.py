"""
Structured output schemas for each crew task. Using `output_pydantic` on every
Task forces CrewAI to validate/coerce the agent's final answer into these exact
shapes — so the pipeline gets reliable typed data back (result.pydantic),
regardless of how chatty or loosely-formatted the underlying LLM's reasoning was.
"""
from typing import Optional

from pydantic import BaseModel, Field


class CropClassificationOutput(BaseModel):
    crop: str = Field(..., description="One of: Mango, Onion, Sugarcane")
    confidence: float = Field(..., description="Model confidence, 0.0-1.0")


class DiseaseDetectionOutput(BaseModel):
    disease_label: Optional[str] = Field(None, description="Raw disease class name, or null if healthy")
    confidence: float = Field(..., description="Ensemble confidence, 0.0-1.0")
    is_healthy: bool
    is_uncertain: bool = Field(False, description="True if EfficientNet and YOLOv8s-cls disagreed on top-1")
    effnet_label: str = ""
    effnet_confidence: float = 0.0
    yolo_label: str = ""
    yolo_confidence: float = 0.0


class LocalizedAdvice(BaseModel):
    summary: str = ""
    symptoms: str = ""
    causes: str = ""
    organic_treatment: str = ""
    chemical_treatment: str = ""
    prevention: str = ""
    severity_note: str = ""
    expert_advice: str = ""


class RecommendationOutput(BaseModel):
    en: LocalizedAdvice
    ur: LocalizedAdvice
