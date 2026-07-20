# PakAgri — ML + RAG + Bilingual Integration

This document covers everything added on top of the original scaffold: real model inference
(replacing the placeholder random logic), a RAG recommendation engine, and English/Urdu support.

**One more real bug caught and fixed**: `api/serializers.py`'s `DiseaseSerializer` referenced
`scientific_name` and `affected_crops` — fields that don't exist on the `Disease` model (only `Crop`
has `scientific_name`). This would have crashed `GET /api/diseases/` immediately on first use. Fixed
to reference the model's actual fields, and now includes the crop relationship.

**Database schema, generated for real**: `DATABASE_SCHEMA.md` (readable summary) and
`pakagri_schema.sql` (raw DDL) were produced by actually installing PostgreSQL, running
`python manage.py migrate` against a real database, and dumping the resulting schema with
`pg_dump` — not written from memory. All 23 tables, confirmed including `ai_content` as a native
`jsonb` column.

## 0. Status: real trained weights are bundled and verified working

`ml_models/` now contains your actual trained weights (copied from your `saved_models/` folder),
and the full pipeline has been tested end-to-end against them:

- All 7 models load correctly (1 crop classifier + 3 crops × EfficientNet+YOLOv8s-cls).
- `sync_ml_metadata` correctly created all **29 disease rows** across the 3 crops, matching your
  models' actual class lists exactly (verified against your real `*_eval_summary.json` files).
- `seed_disease_content` filled draft KB text for **28 of 29** rows automatically.
- A full `DetectionService.process_scan()` run (crop → disease ensemble → DB resolution → Grad-CAM
  image generation) was tested against a sample image and completed successfully.
- The RAG engine's graceful fallback (no `OPENAI_API_KEY` set) was verified to work correctly.

**Two real bugs were caught and fixed during this integration**, both in the class-name-cleaning
logic (`core/management/commands/sync_ml_metadata.py`) — your actual trained class lists exposed
naming patterns I hadn't accounted for:
1. `Caterpillar-P` and similar `-P`/other single-letter tag suffixes weren't being stripped (only
   `-D` was handled before) — generalized to strip any trailing single-letter tag.
2. `BacterialBlights` / `RedRot` (PascalCase with no separator at all) weren't being split into
   readable words — added a PascalCase-splitting step.

**One thing for you to review manually:** your Onion class list includes `onion1`, which doesn't
look like a real disease name (likely a leftover/misc folder from data collection). It's been
created as a `Disease` row (needed so the app can handle it if the model ever predicts it), but it
has no draft content and is flagged `needs_content=True` — worth checking your original dataset to
confirm whether this class should be renamed, merged into another class, or excluded from a future
retraining pass.

## 1. What changed, file by file

| Area | Files | What it does |
|---|---|---|
| Dependencies | `requirements.txt` | Added torch, torchvision, timm, ultralytics, albumentations, opencv-python-headless, openai |
| Settings | `config/settings/base.py`, `.env.example` | `ML_MODELS_DIR`, `ML_DEVICE`, `OPENAI_API_KEY`, `LANGUAGES`/`LOCALE_PATHS`, `LocaleMiddleware`, i18n context processor |
| URLs | `config/urls.py` | Wrapped page routes in `i18n_patterns()` so `/ur/...` serves the Urdu version; `/i18n/` powers the language switcher |
| Model weights | `ml_models/` (new) | Where you copy your Colab-trained `.pth`/`.pt` files — see `ml_models/README.md` |
| ML engine | `detection/ml/` (new: `registry.py`, `inference.py`, `transforms.py`, `gradcam.py`) | Loads models once, runs the crop classifier + per-crop EfficientNet+YOLOv8s-cls ensemble, generates the Grad-CAM visualization |
| Detection service | `detection/services.py` (rewritten) | Now calls the real ML engine instead of `random.choice(...)`; resolves predictions to `Disease` rows; saves the Grad-CAM image |
| Database | `core/models.py`, `detection/models.py`, `recommendation/models.py` + new migrations | Fixed a real bug (Disease name/slug were globally unique, but names like "Rust" and "Healthy" legitimately repeat across crops); added `raw_class_name`, `needs_content`, `is_uncertain`, model-agreement fields, `analysis_image`, `ai_content` (RAG cache) |
| DB sync | `core/management/commands/sync_ml_metadata.py` (new) | Reads your models' actual class lists and creates/updates `Crop`/`Disease` rows — the authoritative way to keep the DB in sync with what the models can actually predict |
| Draft content | `core/management/commands/seed_disease_content.py` (new) | Fills in starter KB text for well-known disease names (non-destructive, review before trusting) |
| RAG engine | `recommendation/rag.py` (new) | Retrieves the `Disease` KB row, calls OpenAI to phrase it warmly in English + Urdu, strictly grounded, with organic/chemical split and an "when to consult an expert" field. Falls back gracefully (never crashes, never loses information) if the API key is missing or the call fails. Exposes a pure `generate_content(context)` function shared by both the direct and CrewAI pipelines |
| Recommendation view | `recommendation/views.py` | Wired in the RAG engine, passes the active language's content to the template |
| **CrewAI pipeline (optional)** | `detection/crew/` (new: `schemas.py`, `tools.py`, `agents.py`, `pipeline.py`), `detection/crew_service.py` (new) | Three agents — Crop Identification, Disease Detection, Agricultural Advisory — run sequentially via CrewAI, each wrapping the exact same underlying code as the direct pipeline (no reimplemented logic). Toggle with `USE_CREWAI_PIPELINE=True` in `.env` |
| Templates | `templates/base/base.html`, `templates/detection/index.html`, `templates/detection/result.html`, `templates/recommendation/detail.html` | Language switcher, RTL layout + Urdu font, loading-overlay animation while a scan processes, model-disagreement warning banner, Grad-CAM visualization display, redesigned recommendation cards (organic/chemical/severity/expert-advice) |

## 2. Setup, in order

```bash
pip install -r requirements.txt
cp .env.example .env
# edit .env: set DJANGO_SECRET_KEY, DATABASE_URL (Postgres), OPENAI_API_KEY

python manage.py migrate

# Copy your Colab-trained files into ml_models/ — see ml_models/README.md for the exact layout
python manage.py sync_ml_metadata      # creates Crop/Disease rows matching your actual trained classes
python manage.py seed_disease_content  # optional: draft KB text for common disease names — REVIEW before trusting

python manage.py createsuperuser
python manage.py runserver
```

Then in `/admin/`, review every `Disease` row where `needs_content` is checked and fill in (or correct)
the description/symptoms/treatment/prevention text — the RAG engine is only as good as this content,
since it's strictly grounded in it and won't invent anything beyond what's there.

## 3. CrewAI multi-agent pipeline (optional)

Three agents, run sequentially by CrewAI, each with exactly one tool:

| Agent | Tool | Wraps |
|---|---|---|
| Crop Identification Specialist | `classify_crop` | `detection/ml/inference.py::predict_crop` (EfficientNet-B0) |
| Plant Disease Detection Specialist | `detect_disease` | `detection/ml/inference.py::predict_disease` (EfficientNet+YOLOv8s-cls ensemble) |
| Agricultural Advisory Specialist | `generate_recommendation` | `recommendation/rag.py::generate_content` (the same grounded OpenAI call the direct pipeline uses) |

Enable it:

```bash
# .env
USE_CREWAI_PIPELINE=True
CREWAI_LLM_MODEL=gpt-4o-mini   # the model each agent uses to reason/orchestrate
```

`detection/services.py::get_detection_service()` picks `CrewDetectionService` or the direct
`DetectionService` based on this flag — nothing else in the codebase needs to change, and both
write to the exact same `Prediction`/`Recommendation` tables.

**Be honest with yourself about the tradeoff before enabling this in production:** the tools call
the identical ML/RAG code either way — CrewAI adds a layer of LLM-driven orchestration *around*
that code, not new capability. Concretely, per scan you get: 3 extra LLM round-trips (one per
agent turn) on top of the model inference time itself, extra OpenAI API cost per scan (not just
per recommendation), and a new failure mode where a confused agent could theoretically call a tool
with a malformed argument. `output_pydantic` on every task guards against garbled *final* output,
but doesn't prevent an agent from occasionally misreading context between steps. For a fixed,
deterministic pipeline like this one (classify → detect → recommend, always in that order), the
direct pipeline is the recommended default. The CrewAI version is genuinely worth it if you plan to
extend the agents with real autonomous decisions later — e.g., an agent that decides whether to
escalate a case to a human agronomist based on severity and confidence, rather than always
following the same three fixed steps.

## 4. Honest limitations to know about

- **CPU inference by default.** Most Django hosts don't have a GPU. `ML_DEVICE=cpu` in `.env` is the
  right default; expect roughly 1-3 seconds per image rather than the sub-second speed you saw on
  Colab's T4. Set `ML_DEVICE=cuda` only if your production server actually has a GPU attached.
- **Grad-CAM box is approximate, not a trained detector.** It's the model's attention region converted
  to a bounding box, not pixel-precise lesion localization — the result page footnotes this honestly.
- **Urdu template strings aren't translated yet** — the switcher and RTL layout work, but `{% trans %}`
  strings need `django-admin makemessages -l ur` + manual translation + `compilemessages` to actually
  show Urdu text (see `locale/README.md`). The RAG-generated recommendation text, however, is already
  real Urdu — that's dynamically generated per-prediction, not a template string.
- **`seed_disease_content` is a draft**, not verified agricultural advice — a farmer may act on this
  directly, so review it (ideally with an agronomist) before relying on it in production.
- **Missing weight files degrade gracefully, not silently** — if `ml_models/disease/onion_effnet_b0_best.pth`
  is absent, Onion predictions fall back to YOLO-only (or fail clearly with a logged warning if neither
  model is present) rather than crashing the request.
