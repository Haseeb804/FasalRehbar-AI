"""
Agent definitions. Each agent is deliberately narrow (single tool, single
responsibility) — a "researcher needs search tools, not file writers" per
CrewAI's own guidance. `allow_delegation=False` on all three since this is a
fixed, sequential pipeline, not a team that should be re-negotiating who does
what.
"""
import os

from django.conf import settings

from crewai import Agent, LLM

from .tools import ClassifyCropTool, DetectDiseaseTool, GenerateRecommendationTool


def _get_llm() -> LLM:
    # litellm (which CrewAI uses under the hood) reads API keys from the process
    # environment, not from Django settings directly — bridge the two here.
    if settings.OPENAI_API_KEY:
        os.environ.setdefault("OPENAI_API_KEY", settings.OPENAI_API_KEY)
    return LLM(
        model=getattr(settings, "CREWAI_LLM_MODEL", "gpt-4o-mini"),
        temperature=0.2,
    )


def build_classification_agent() -> Agent:
    return Agent(
        role="Crop Identification Specialist",
        goal="Accurately identify which crop — Mango, Onion, or Sugarcane — appears in an uploaded farm image.",
        backstory=(
            "You are an agricultural computer-vision specialist. You always use the classify_crop "
            "tool rather than guessing from the file name or your own assumptions — the tool runs "
            "a trained EfficientNet-B0 model and is the only reliable source of truth here."
        ),
        tools=[ClassifyCropTool()],
        llm=_get_llm(),
        allow_delegation=False,
        verbose=getattr(settings, "DEBUG", False),
    )


def build_detection_agent() -> Agent:
    return Agent(
        role="Plant Disease Detection Specialist",
        goal=(
            "Given the crop identified in the previous step, determine whether the plant is "
            "healthy or diseased, and if diseased, identify the specific disease."
        ),
        backstory=(
            "You are a plant pathology specialist supported by an ensemble of two trained "
            "classifiers (EfficientNet-B0 and YOLOv8s-cls). You always call the detect_disease "
            "tool with the exact image_path and crop_name from the classification step — never "
            "guess a disease yourself. If the tool reports the two models disagreed, you report "
            "that honestly rather than picking one arbitrarily."
        ),
        tools=[DetectDiseaseTool()],
        llm=_get_llm(),
        allow_delegation=False,
        verbose=getattr(settings, "DEBUG", False),
    )


def build_recommendation_agent() -> Agent:
    return Agent(
        role="Agricultural Advisory Specialist",
        goal=(
            "Provide clear, actionable, bilingual (English and Urdu) treatment and prevention "
            "advice for the diagnosed crop/disease, strictly grounded in the knowledge base."
        ),
        backstory=(
            "You are an agricultural extension advisor who communicates with farmers who may not "
            "have formal training. You always call the generate_recommendation tool with the crop, "
            "disease, and confidence/agreement details from the previous steps — you never invent "
            "treatment advice yourself, since incorrect guidance (e.g. wrong dosages) could cause "
            "real harm to a farmer's crop or their livelihood."
        ),
        tools=[GenerateRecommendationTool()],
        llm=_get_llm(),
        allow_delegation=False,
        verbose=getattr(settings, "DEBUG", False),
    )
