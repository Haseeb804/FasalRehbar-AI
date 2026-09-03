"""
RAG (Retrieval-Augmented Generation) & Evidence-Based Recommendation Engine for FasalRehbar AI.

Retrieval Stage:
  Retrieves scientifically verified agronomic guidance, growth stage vulnerability,
  practical containment checklists, water/nutrient management protocols, 7-day timelines,
  and official citations (PARC, Agri Extension, UAF, FAO) from `recommendation.knowledge_base`.

Generation Stage:
  Prompts the LLM (OpenAI / OpenRouter) to deliver a farmer-friendly, structured advisory
  in both English and Urdu. Strictly forbids ungrounded hallucinations, unverified chemical
  dosages, or unsupported citations.

Fallback Guarantee:
  If the LLM or API is offline/unavailable, `_fallback_content()` returns 100% of the structured
  knowledge-base guidance with complete 7-day timelines and verified citations.
"""
import json
import logging
from typing import Any, Dict

from django.conf import settings
from django.utils import timezone

from .knowledge_base import get_agri_knowledge

logger = logging.getLogger("pakagri.rag")


SYSTEM_PROMPT = """You are an expert Senior Agricultural Extension Specialist assisting farmers in Pakistan.
You are generating an evidence-based, actionable Crop Health Intelligence Advisory based strictly on the \
provided "Retrieved Agricultural Knowledge & Evidence".

CRITICAL INSTRUCTIONS:
1. Ground your recommendations STRICTLY in the provided agricultural evidence.
2. DO NOT hallucinate facts, invent unverified chemical trade names, or specify ungrounded pesticide dosages.
3. Always emphasize safe agricultural practices, personal protective equipment (PPE), and adhering to local agricultural extension officer labels.
4. Keep the tone respectful, clear, warm, and easily understood by non-technical farmers.
5. Output ONLY a valid JSON object (no markdown backticks, no markdown code blocks, no extraneous text) with the exact structure below:

{
  "en": {
    "summary": "Concise 2-sentence executive diagnosis summary",
    "growth_stage": "Affected growth stage context",
    "what_this_means": "Clear explanation answering: What is happening? Why it matters? Symptoms to monitor.",
    "immediate_actions": [
      "Action 1 (inspection & isolation)",
      "Action 2 (sanitation / cultural action)",
      "Action 3 (drainage / aeration)",
      "Action 4 (monitoring)"
    ],
    "water_management": "Specific irrigation considerations, moisture risks, and drainage protocol",
    "nutrient_management": "Nutrient balance guidance (Nitrogen moderation, Potash/Phosphorus, Micronutrients)",
    "disease_management": {
      "cultural": "Sanitation, row spacing, pruning, crop rotation",
      "biological": "Bio-protectants (Trichoderma, Bacillus, Neem extracts)",
      "chemical": "Approved chemical groups with strict disclaimer to follow local extension labels"
    },
    "action_plan_7day": {
      "today": "Day 1 immediate inspection, isolation, and sanitization",
      "day_2_3": "Days 2-3 moisture adjustment, airflow, protective application",
      "day_4_5": "Days 4-5 symptom progression evaluation and perimeter check",
      "day_6_7": "Days 6-7 health reassessment and recovery audit"
    },
    "warning_signs": "Critical signs indicating rapid disease spread requiring emergency containment",
    "expert_advice": "Clear threshold criteria and advice on when to contact local extension services",
    "evidence_sources": [
      {
        "organization": "Institution Name (e.g. PARC, UAF, FAO, CABI)",
        "document": "Document or Guide Title",
        "focus": "Core recommendation supported",
        "reference": "Official reference code or manual"
      }
    ]
  },
  "ur": {
    "summary": "... (Urdu translation of executive summary) ...",
    "growth_stage": "... (Urdu) ...",
    "what_this_means": "... (Urdu) ...",
    "immediate_actions": [ "... (Urdu actions) ..." ],
    "water_management": "... (Urdu) ...",
    "nutrient_management": "... (Urdu) ...",
    "disease_management": {
      "cultural": "... (Urdu) ...",
      "biological": "... (Urdu) ...",
      "chemical": "... (Urdu) ..."
    },
    "action_plan_7day": {
      "today": "... (Urdu) ...",
      "day_2_3": "... (Urdu) ...",
      "day_4_5": "... (Urdu) ...",
      "day_6_7": "... (Urdu) ..."
    },
    "warning_signs": "... (Urdu) ...",
    "expert_advice": "... (Urdu) ...",
    "evidence_sources": [
      {
        "organization": "ادارہ کا نام (مثلاً زرعی تحقیقاتی کونسل / محکمہ زراعت)",
        "document": "دستاویز / گائیڈ کا نام",
        "focus": "سفارش کی بنیادی تفصیل",
        "reference": "حوالہ"
      }
    ]
  }
}"""


def _build_user_prompt(context: dict) -> str:
    kb = context["agri_knowledge"]
    lines = [
        f"Crop: {context['crop_name']}",
        f"Diagnosis: {'Healthy (No Disease Detected)' if context['is_healthy'] else context.get('disease_name', 'Unknown Condition')}",
        f"Confidence Score: {context['confidence']:.1%}",
    ]

    if context.get("is_uncertain"):
        lines.append(
            f"NOTE: ML Detection models indicated uncertainty (EfficientNet: '{context.get('effnet_label')}' vs YOLOv8: '{context.get('yolo_label')}'). "
            f"Acknowledge this uncertainty clearly in the summary and expert advice."
        )

    lines.append("\n=== Retrieved Agricultural Knowledge & Evidence ===")
    lines.append(f"Scientific Pathogen/Context: {kb.get('scientific_name')}")
    lines.append(f"Severity Rating: {kb.get('severity')}")
    lines.append(f"Vulnerable Growth Stage: {kb.get('growth_stage_vulnerability')}")
    lines.append(f"Agronomic Meaning: {kb.get('what_this_means_en')}")
    lines.append(f"Immediate Action Checklist: {', '.join(kb.get('immediate_actions_en', []))}")
    lines.append(f"Water Protocol: {kb.get('water_management_en')}")
    lines.append(f"Nutrient Protocol: {kb.get('nutrient_management_en')}")
    lines.append(f"Disease Management Cultural: {kb.get('disease_management_en', {}).get('cultural')}")
    lines.append(f"Disease Management Biological: {kb.get('disease_management_en', {}).get('biological')}")
    lines.append(f"Disease Management Chemical: {kb.get('disease_management_en', {}).get('chemical')}")
    lines.append(f"7-Day Timeline Today: {kb.get('action_plan_7day_en', {}).get('today')}")
    lines.append(f"7-Day Timeline Days 2-3: {kb.get('action_plan_7day_en', {}).get('day_2_3')}")
    lines.append(f"7-Day Timeline Days 4-5: {kb.get('action_plan_7day_en', {}).get('day_4_5')}")
    lines.append(f"7-Day Timeline Days 6-7: {kb.get('action_plan_7day_en', {}).get('day_6_7')}")
    lines.append(f"Warning Signs: {kb.get('warning_signs_en')}")
    lines.append(f"Expert Escalation: {kb.get('expert_escalation_en')}")
    lines.append(f"Authoritative Sources: {json.dumps(kb.get('evidence_sources', []))}")

    return "\n".join(lines)


def _fallback_content(context: dict) -> dict:
    """
    Constructs a complete, 100% structured bilingual recommendation directly from the
    verified Agricultural Knowledge Base when LLM is offline or API key is absent.
    """
    kb = context["agri_knowledge"]
    crop_name = context["crop_name"]
    is_healthy = context["is_healthy"]

    # English structured block
    en = {
        "summary": (
            f"The {crop_name} plant shows robust health with no active disease symptoms."
            if is_healthy
            else f"{kb.get('condition_name')} identified on {crop_name} with {context['confidence']:.0%} confidence. Severity: {kb.get('severity', 'moderate').upper()}."
        ),
        "growth_stage": kb.get("growth_stage_vulnerability", "Vegetative to Maturity"),
        "what_this_means": kb.get("what_this_means_en", ""),
        "immediate_actions": kb.get("immediate_actions_en", []),
        "water_management": kb.get("water_management_en", ""),
        "nutrient_management": kb.get("nutrient_management_en", ""),
        "disease_management": kb.get("disease_management_en", {
            "cultural": "Maintain optimal row spacing and clean field borders.",
            "biological": "Use bio-protectants during early growth.",
            "chemical": "Follow registered agricultural extension guidance."
        }),
        "action_plan_7day": kb.get("action_plan_7day_en", {
            "today": "Inspect neighboring plants and confirm condition scope.",
            "day_2_3": "Adjust irrigation drainage and field aeration.",
            "day_4_5": "Check newly emerging foliage for clean growth.",
            "day_6_7": "Reassess crop health; consult extension officer if needed."
        }),
        "warning_signs": kb.get("warning_signs_en", "Rapid spreading of discolouration or lodging."),
        "expert_advice": kb.get("expert_escalation_en", "Contact your local agricultural extension officer for on-field diagnosis."),
        "evidence_sources": kb.get("evidence_sources", [])
    }

    # Urdu structured block
    ur = {
        "summary": (
            f"{crop_name} کی فصل صحت مند اور بیماری سے پاک ہے۔"
            if is_healthy
            else f"{kb.get('condition_name_ur')} کی نشاندہی ({context['confidence']:.0%} فیصد یقین کے ساتھ)۔ شدت: {kb.get('severity', 'moderate')}."
        ),
        "growth_stage": kb.get("growth_stage_vulnerability", "بڑھوتری تا پختگی"),
        "what_this_means": kb.get("what_this_means_ur", ""),
        "immediate_actions": kb.get("immediate_actions_ur", []),
        "water_management": kb.get("water_management_ur", ""),
        "nutrient_management": kb.get("nutrient_management_ur", ""),
        "disease_management": kb.get("disease_management_ur", {
            "cultural": "پودوں میں مناسب فاصلہ رکھیں اور کھیت کو جڑی بوٹیوں سے پاک رکھیں۔",
            "biological": "ابتدائی مرحلے پر بائیو فنگسائڈز کا استعمال کریں۔",
            "chemical": "محکمہ زراعت کی تجویز کردہ ادویات کا محفوظ استعمال کریں۔"
        }),
        "action_plan_7day": kb.get("action_plan_7day_ur", {
            "today": "کھیت کا معائنہ کریں اور متاثرہ حصے کی نشاندہی کریں۔",
            "day_2_3": "پانی کی نکاسی درست کریں اور حفاظتی اقدام کریں۔",
            "day_4_5": "نئے پتوں کی صحت کا جائزہ لیں۔",
            "day_6_7": "فصل کی بحالی کی تصدیق کریں اور ماہر سے مشورہ کریں۔"
        }),
        "warning_signs": kb.get("warning_signs_ur", "پودوں کا تیزی سے سوکھنا یا داغوں کا پھیلنا۔"),
        "expert_advice": kb.get("expert_escalation_ur", "شدید علامات کی صورت میں فوری مقامی محکمہ زراعت سے رابطہ کریں۔"),
        "evidence_sources": [
            {
                "organization": s.get("organization", "زرعی تحقیقی ادارہ"),
                "document": s.get("document", "زرعی رہنما گائیڈ"),
                "focus": s.get("focus", "فصل کی حفاظت کی سفارشات"),
                "reference": s.get("reference", "حوالہ")
            }
            for s in kb.get("evidence_sources", [])
        ]
    }

    return {"en": en, "ur": ur}


def generate_content(context: dict) -> dict:
    """
    Core RAG function: Retrieves deep knowledge-base context and generates
    structured bilingual recommendations using LLM, with fallback guarantee.
    """
    if not getattr(settings, "RAG_ENABLED", False):
        return _fallback_content(context)

    try:
        from openai import OpenAI

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
            temperature=0.3,
            response_format={"type": "json_object"},
        )
        raw = response.choices[0].message.content
        content = json.loads(raw)

        if "en" not in content or "ur" not in content:
            raise ValueError(f"LLM response missing 'en' or 'ur' root keys: {list(content.keys())}")

        # Ensure evidence_sources is always preserved from knowledge base if LLM truncated it
        kb_sources = context["agri_knowledge"].get("evidence_sources", [])
        if not content["en"].get("evidence_sources"):
            content["en"]["evidence_sources"] = kb_sources

        return content

    except Exception:
        logger.exception("RAG generation failed for context crop=%s disease=%s — using structured fallback",
                         context.get("crop_name"), context.get("disease_name"))
        return _fallback_content(context)


def generate_recommendation(recommendation) -> dict:
    """
    Generates or retrieves cached rich bilingual recommendations for a Prediction.
    """
    if recommendation.ai_content and "en" in recommendation.ai_content and "immediate_actions" in recommendation.ai_content["en"]:
        return recommendation.ai_content

    prediction = recommendation.prediction
    disease = recommendation.disease
    crop_name = prediction.crop.name if prediction.crop else "Onion"
    disease_name = disease.name if disease else (prediction.yolo_top_label or "")

    agri_kb = get_agri_knowledge(
        crop=crop_name,
        disease_name_or_label=disease_name,
        is_healthy=prediction.is_healthy
    )

    context = {
        "crop_name": crop_name,
        "disease_name": disease_name,
        "is_healthy": prediction.is_healthy,
        "confidence": prediction.confidence_score,
        "is_uncertain": prediction.is_uncertain,
        "effnet_label": prediction.effnet_top_label,
        "effnet_confidence": prediction.effnet_top_confidence,
        "yolo_label": prediction.yolo_top_label,
        "yolo_confidence": prediction.yolo_top_confidence,
        "agri_knowledge": agri_kb,
    }

    content = generate_content(context)

    recommendation.ai_content = content
    recommendation.ai_content_generated_at = timezone.now()
    recommendation.ai_generation_error = "" if getattr(settings, "RAG_ENABLED", False) else (
        "RAG grounded directly via Knowledge Base (OpenAI key not configured)."
    )
    recommendation.save(update_fields=["ai_content", "ai_content_generated_at", "ai_generation_error"])
    return content
