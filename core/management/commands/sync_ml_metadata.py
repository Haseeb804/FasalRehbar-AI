"""
Reads the class lists your Colab notebooks actually trained on (from
eval_metrics.json / *_eval_summary.json under ML_MODELS_DIR) and creates/updates
matching Crop and Disease rows in the database.

This is the authoritative source for disease names — it never requires guessing
or hand-typing the exact class list, and it never overwrites knowledge-base text
(description/symptoms/treatment/etc.) you've already filled in for an existing
disease. Newly-created rows are flagged `needs_content=True` so they're easy to
find in the admin and fill in.

Usage:
    python manage.py sync_ml_metadata
"""
import json
import re
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from core.models import Crop, Disease

CROPS = ["Mango", "Onion", "Sugarcane"]

CROP_DEFAULTS = {
    "Mango": {
        "scientific_name": "Mangifera indica",
        "description": "Mango is a tropical fruit tree widely cultivated in Pakistan.",
    },
    "Onion": {
        "scientific_name": "Allium cepa",
        "description": "Onion is a widely cultivated bulb crop in Pakistan.",
    },
    "Sugarcane": {
        "scientific_name": "Saccharum officinarum",
        "description": "Sugarcane is an important cash crop grown in Pakistan.",
    },
}

# Suffixes that show up in raw dataset folder names but shouldn't appear in a
# farmer-facing display name (e.g. "Alternaria_D" -> "Alternaria",
# "Caterpillar-P" -> "Caterpillar"). The single-letter tag pattern covers any
# such suffix generically rather than hardcoding each one seen so far.
_STRIP_SUFFIXES = [r"_augment$", r"[_\-][A-Za-z]$"]


def clean_display_name(raw_class_name: str) -> str:
    name = raw_class_name.strip()
    for pattern in _STRIP_SUFFIXES:
        name = re.sub(pattern, "", name, flags=re.IGNORECASE)

    # Split PascalCase/camelCase words that have no separator at all
    # (e.g. "BacterialBlights" -> "Bacterial Blights", "RedRot" -> "Red Rot")
    name = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", name)

    name = name.replace("_", " ").replace("-", " ")
    name = re.sub(r"\s+", " ", name).strip()

    if name.lower() in ("healthy", "healthy leaves"):
        return "Healthy"

    # Title-case each word, but don't mangle words that are already all-caps
    # (acronyms) or already mixed-case in a meaningful way.
    words = []
    for word in name.split(" "):
        if word.isupper() and len(word) > 1:
            words.append(word)
        else:
            words.append(word.capitalize())
    return " ".join(words)


class Command(BaseCommand):
    help = "Sync Crop/Disease database rows from the trained models' actual class lists."

    def handle(self, *args, **options):
        models_dir = Path(settings.ML_MODELS_DIR)

        # ── Crops (mostly static, but keep in one place) ────────────────────
        crop_objs = {}
        for crop_name in CROPS:
            defaults = CROP_DEFAULTS.get(crop_name, {})
            crop, created = Crop.objects.get_or_create(name=crop_name, defaults=defaults)
            crop_objs[crop_name] = crop
            self.stdout.write(self.style.SUCCESS(f"{'Created' if created else 'Found'} crop: {crop_name}"))

        # ── Diseases, per crop, from *_eval_summary.json ────────────────────
        disease_dir = models_dir / "disease"
        total_created, total_found = 0, 0

        for crop_name in CROPS:
            tag = crop_name.lower()
            summary_path = disease_dir / f"{tag}_eval_summary.json"

            if not summary_path.exists():
                self.stdout.write(self.style.WARNING(
                    f"  [{crop_name}] {summary_path} not found — skipping. "
                    f"Copy your notebook's saved_models/disease/ files into ml_models/disease/ first."
                ))
                continue

            try:
                with open(summary_path) as f:
                    data = json.load(f)
                classes = data["classes"]
            except (json.JSONDecodeError, KeyError) as exc:
                self.stdout.write(self.style.ERROR(f"  [{crop_name}] Could not read classes from {summary_path}: {exc}"))
                continue

            crop = crop_objs[crop_name]
            for raw_class_name in classes:
                display_name = clean_display_name(raw_class_name)
                slug_base = slugify(f"{crop_name}-{display_name}")

                disease, created = Disease.objects.get_or_create(
                    crop=crop,
                    raw_class_name=raw_class_name,
                    defaults={
                        "name": display_name,
                        "slug": slug_base,
                        "needs_content": display_name != "Healthy",
                        "severity": Disease.Severity.MEDIUM,
                    },
                )
                if created:
                    total_created += 1
                    self.stdout.write(f"    + {crop_name}: created '{display_name}' (raw: {raw_class_name})")
                else:
                    total_found += 1

        self.stdout.write(self.style.SUCCESS(
            f"\nDone. {total_created} disease row(s) created, {total_found} already existed."
        ))
        if total_created:
            self.stdout.write(self.style.WARNING(
                "Newly created diseases have `needs_content=True` — fill in their description/symptoms/"
                "treatment/prevention in the admin, or run `python manage.py seed_disease_content` for a "
                "draft starting point on commonly-known disease names."
            ))
