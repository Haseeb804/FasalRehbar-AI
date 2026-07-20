"""
Wires the three agents into a sequential Crew: classification -> detection ->
recommendation, each task receiving the prior tasks' outputs as context.

`output_pydantic` on every Task forces CrewAI to validate/coerce the final
answer into our schemas (schemas.py) — so run_pipeline() always returns clean,
typed objects, regardless of how the underlying LLM phrased its response.
"""
import logging

from crewai import Crew, Process, Task

from .agents import build_classification_agent, build_detection_agent, build_recommendation_agent
from .schemas import CropClassificationOutput, DiseaseDetectionOutput, RecommendationOutput

logger = logging.getLogger("pakagri.crew")


def run_pipeline(image_path: str) -> dict:
    """
    Runs the full 3-agent pipeline for one image. Returns:
        {
            "classification": CropClassificationOutput,
            "detection": DiseaseDetectionOutput,
            "recommendation": RecommendationOutput,
        }
    Raises on failure — the caller (CrewDetectionService) is responsible for
    catching and logging, same as the direct pipeline's error handling.
    """
    classification_agent = build_classification_agent()
    detection_agent = build_detection_agent()
    recommendation_agent = build_recommendation_agent()

    task_classify = Task(
        description=(
            f"Identify which crop appears in the image located at exactly this path: '{image_path}'. "
            f"Call the classify_crop tool with image_path='{image_path}'."
        ),
        expected_output="The identified crop name and confidence score.",
        agent=classification_agent,
        output_pydantic=CropClassificationOutput,
    )

    task_detect = Task(
        description=(
            f"Using the crop identified in the previous task and the same image path "
            f"'{image_path}', call the detect_disease tool with image_path='{image_path}' and "
            f"crop_name set to the exact crop name determined previously. Report whether the "
            f"plant is healthy, and if not, which disease, plus whether the two underlying "
            f"models agreed."
        ),
        expected_output="Disease label (or healthy status), confidence, and model-agreement details.",
        agent=detection_agent,
        context=[task_classify],
        output_pydantic=DiseaseDetectionOutput,
    )

    task_recommend = Task(
        description=(
            "Using the crop and disease detection results from the previous two tasks, call the "
            "generate_recommendation tool with the crop name, disease label (or is_healthy=true "
            "with no disease_label), confidence, and the model-agreement fields (is_uncertain, "
            "effnet_label, effnet_confidence, yolo_label, yolo_confidence) to produce bilingual "
            "(English and Urdu) treatment guidance for the farmer."
        ),
        expected_output="Bilingual (English and Urdu) structured advice.",
        agent=recommendation_agent,
        context=[task_classify, task_detect],
        output_pydantic=RecommendationOutput,
    )

    crew = Crew(
        agents=[classification_agent, detection_agent, recommendation_agent],
        tasks=[task_classify, task_detect, task_recommend],
        process=Process.sequential,
        verbose=False,
    )

    crew.kickoff()

    classification = task_classify.output.pydantic
    detection = task_detect.output.pydantic
    recommendation = task_recommend.output.pydantic

    if classification is None or detection is None or recommendation is None:
        raise RuntimeError(
            "CrewAI pipeline did not produce valid structured output for one or more stages "
            "(classification/detection/recommendation)."
        )

    return {
        "classification": classification,
        "detection": detection,
        "recommendation": recommendation,
    }
