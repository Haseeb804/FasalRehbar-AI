"""
RAG (Retrieval-Augmented Generation) recommendation engine.

Retrieval step: the "knowledge base" is the Disease model itself (description,
symptoms, causes, treatment, prevention, severity) — already structured, admin-
editable, and the authoritative source of truth. This module retrieves that row
and feeds it to the LLM as strict grounding context.

Generation step: OpenAI is prompted to phrase that same information warmly and
clearly in both English and Urdu, split into organic vs. chemical treatment
options, and to explicitly flag when to consult a human agricultural expert.
The prompt forbids inventing anything not present in the retrieved KB row —
this is a farmer-facing tool, so ungrounded generation (invented dosages, made-
up facts) is not an acceptable trade-off for a more polished-sounding answer.

If OPENAI_API_KEY isn't configured, or the API call fails for any reason, this
degrades gracefully: the recommendation page falls back to showing the raw KB
fields directly rather than losing information or erroring out.
"""
import json
import logging

from django.conf import settings
from django.utils import timezone

logger = logging.getLogger("pakagri.rag")


SYSTEM_PROMPT = """You are an agricultural assistant helping Pakistani farmers understand a crop disease \
diagnosis from an AI image classifier. You MUST ground your answer strictly in the "Knowledge base entry" \
provided below — do not invent facts, dosages, product names, or details not present in it. If the knowledge \
base entry is thin or missing a field, say so plainly rather than filling it in from general knowledge, and \
recommend consulting a local agricultural extension officer for specifics like exact dosages.

Write in a warm, clear, respectful tone suitable for a farmer who may not have formal agricultural training. \
Keep each field concise (2-4 sentences, or a short list where natural).

Respond with ONLY a JSON object (no markdown fences, no commentary) with this exact shape:
{
  "en": {
    "summary": "...",
    "symptoms": "...",
    "causes": "...",
    "organic_treatment": "...",
    "chemical_treatment": "...",
    "prevention": "...",
    "severity_note": "...",
    "expert_advice": "..."
  },
  "ur": { ... same keys, written in Urdu ... }
}"""


def _build_user_prompt(context: dict) -> str:
    kb = context["knowledge_base"]
    lines = [
        f"Crop: {context['crop_name']}",
        f"Diagnosis: {'Healthy (no disease detected)' if context['is_healthy'] else kb.get('name', 'Unknown')}",
        f"Model confidence: {context['confidence']:.0%}",
    ]
    if context.get("is_uncertain"):
        lines.append(
            f"NOTE: the two detection models disagreed — EfficientNet predicted "
            f"'{context['effnet_label']}' ({context['effnet_confidence']:.0%}) while YOLOv8s-cls predicted "
            f"'{context['yolo_label']}' ({context['yolo_confidence']:.0%}). Reflect this uncertainty honestly "
            f"in your summary and expert_advice fields rather than presenting a single confident diagnosis."
        )

    if not context["is_healthy"]:
        lines.append("\nKnowledge base entry:")
        lines.append(f"- Description: {kb.get('description') or '(not available)'}")
        lines.append(f"- Symptoms: {kb.get('symptoms') or '(not available)'}")
        lines.append(f"- Causes: {kb.get('causes') or '(not available)'}")
        lines.append(f"- Treatment: {kb.get('treatment') or '(not available)'}")
        lines.append(f"- Prevention: {kb.get('prevention') or '(not available)'}")
        lines.append(f"- Severity: {kb.get('severity') or '(not available)'}")

    return "\n".join(lines)


def _fallback_content(context: dict) -> dict:
    """Used when RAG is disabled or the API call fails — never lose information."""
    kb = context["knowledge_base"]
    if context["is_healthy"]:
        en = {
            "summary": "No disease was detected — this plant appears healthy.",
            "symptoms": "No visible symptoms of disease.",
            "causes": "Not applicable.",
            "organic_treatment": "No treatment needed.",
            "chemical_treatment": "No treatment needed.",
            "prevention": "Maintain proper irrigation, balanced fertilization, and regular monitoring.",
            "severity_note": "None — plant health looks good.",
            "expert_advice": "Continue routine monitoring; consult an expert if symptoms appear later.",
        }
    else:
        en = {
            "summary": kb.get("description") or "No description available for this disease yet.",
            "symptoms": kb.get("symptoms") or "Not documented yet.",
            "causes": kb.get("causes") or "Not documented yet.",
            "organic_treatment": kb.get("treatment") or "Not documented yet.",
            "chemical_treatment": kb.get("treatment") or "Not documented yet.",
            "prevention": kb.get("prevention") or "Not documented yet.",
            "severity_note": f"Severity: {kb.get('severity', 'unknown')}.",
            "expert_advice": "Please consult a local agricultural extension officer for confirmation and precise treatment guidance.",
        }
    return {"en": en, "ur": en}  # no Urdu translation available in fallback mode


def generate_content(context: dict) -> dict:
    """
    Pure, DB-independent core of the RAG engine: given a context dict (crop name,
    healthy/disease state, confidence, model-agreement info, and the retrieved
    knowledge-base fields), returns bilingual {"en": {...}, "ur": {...}} advice.

    This is the single source of truth for the grounded-generation logic, used by:
    - generate_recommendation() below (the direct, non-agentic path)
    - detection/crew/tools.py's RecommendationTool (the CrewAI agentic path)
    so the prompt and fallback behavior never drift between the two pipelines.
    """
    if not getattr(settings, "RAG_ENABLED", False):
        return _fallback_content(context)

    try:
        from openai import OpenAI

        # Support both OpenAI and OpenRouter (or any OpenAI-compatible provider).
        # OPENAI_BASE_URL is set to https://openrouter.ai/api/v1 for OpenRouter keys.
        client_kwargs = {"api_key": settings.OPENAI_API_KEY}
        base_url = getattr(settings, "OPENAI_BASE_URL", "")
        if base_url:
            client_kwargs["base_url"] = base_url

        client = OpenAI(**client_kwargs)

        response = client.chat.completions.create(
            model=getattr(settings, "OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": _build_user_prompt(context)},
            ],
            temperature=0.4,
            response_format={"type": "json_object"},
        )
        raw = response.choices[0].message.content
        content = json.loads(raw)

        if "en" not in content or "ur" not in content:
            raise ValueError(f"LLM response missing expected 'en'/'ur' keys: {list(content.keys())}")

        return content

    except Exception:
        logger.exception("RAG generation failed for context crop=%s", context.get("crop_name"))
        return _fallback_content(context)



def generate_recommendation(recommendation) -> dict:
    """
    Generates (or returns cached) bilingual RAG content for a Recommendation.
    Always returns a dict with "en"/"ur" keys — never raises to the caller.
    """
    if recommendation.ai_content:
        return recommendation.ai_content  # already cached from a previous call

    prediction = recommendation.prediction
    disease = recommendation.disease

    context = {
        "crop_name": prediction.crop.name if prediction.crop else "Unknown crop",
        "is_healthy": prediction.is_healthy,
        "confidence": prediction.confidence_score,
        "is_uncertain": prediction.is_uncertain,
        "effnet_label": prediction.effnet_top_label,
        "effnet_confidence": prediction.effnet_top_confidence,
        "yolo_label": prediction.yolo_top_label,
        "yolo_confidence": prediction.yolo_top_confidence,
        "knowledge_base": {
            "name": disease.name if disease else None,
            "description": disease.description if disease else "",
            "symptoms": disease.symptoms if disease else "",
            "causes": disease.causes if disease else "",
            "treatment": disease.treatment if disease else "",
            "prevention": disease.prevention if disease else "",
            "severity": disease.get_severity_display() if disease else "",
        },
    }

    content = generate_content(context)

    recommendation.ai_content = content
    recommendation.ai_content_generated_at = timezone.now()
    recommendation.ai_generation_error = "" if getattr(settings, "RAG_ENABLED", False) else (
        "RAG disabled (no OPENAI_API_KEY configured) — showing KB fallback."
    )
    recommendation.save(update_fields=["ai_content", "ai_content_generated_at", "ai_generation_error"])
    return content
