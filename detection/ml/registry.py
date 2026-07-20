"""
Lazy singleton registry for all ML models used by PakAgri.

Models are loaded once (on first request that needs them) and cached in memory
for the lifetime of the Django process — loading a fresh EfficientNet-B0 or
YOLOv8s-cls checkpoint per request would be far too slow.

Any missing weight file is handled gracefully: it's logged as a warning and
that specific model is simply unavailable (predict_* functions in inference.py
degrade to whichever model(s) *are* available, rather than crashing the request).
"""
import json
import logging
import threading
from pathlib import Path

from django.conf import settings

logger = logging.getLogger("pakagri.ml")

_lock = threading.Lock()
_registry = None  # populated lazily by get_registry()


class DiseaseModelSet:
    """Holds the (optional) EfficientNet + YOLOv8s-cls pair for one crop."""

    def __init__(self, crop_name, classes, effnet_model=None, yolo_model=None):
        self.crop_name = crop_name
        self.classes = classes  # exact training-time class order (from *_eval_summary.json)
        self.effnet_model = effnet_model
        self.yolo_model = yolo_model

    @property
    def has_effnet(self):
        return self.effnet_model is not None

    @property
    def has_yolo(self):
        return self.yolo_model is not None

    @property
    def is_available(self):
        return self.has_effnet or self.has_yolo


class ModelRegistry:
    def __init__(self):
        self.device = None
        self.crop_classifier = None
        self.crop_classes = []
        self.disease_models = {}  # crop_name -> DiseaseModelSet

    # ── loading helpers ──────────────────────────────────────────────────
    def _read_classes_json(self, json_path):
        try:
            with open(json_path) as f:
                data = json.load(f)
            # eval_metrics.json (crop classifier) uses "classes" directly;
            # *_eval_summary.json (disease models) also uses "classes" at top level.
            classes = data.get("classes")
            if classes:
                return classes
        except FileNotFoundError:
            logger.warning("Class list file not found: %s", json_path)
        except (json.JSONDecodeError, KeyError) as exc:
            logger.warning("Could not parse class list file %s: %s", json_path, exc)
        return None

    def _load_effnet(self, weights_path, num_classes):
        import torch
        import timm

        if not Path(weights_path).exists():
            logger.warning("EfficientNet weights not found: %s", weights_path)
            return None
        try:
            ckpt = torch.load(weights_path, map_location=self.device, weights_only=False)
            model = timm.create_model("efficientnet_b0", pretrained=False, num_classes=num_classes)
            model.load_state_dict(ckpt["model_state_dict"])
            model = model.to(self.device).eval()
            logger.info("✓ Loaded EfficientNet-B0 (%d classes): %s", num_classes, Path(weights_path).name)
            return model
        except Exception:
            logger.exception("Failed to load EfficientNet weights: %s", weights_path)
            return None

    def _load_yolo(self, weights_path):
        if not Path(weights_path).exists():
            logger.warning("YOLOv8s-cls weights not found: %s", weights_path)
            return None
        try:
            from ultralytics import YOLO
            model = YOLO(str(weights_path))
            logger.info("✓ Loaded YOLOv8s-cls: %s", Path(weights_path).name)
            return model
        except Exception:
            logger.exception("Failed to load YOLOv8s-cls weights: %s", weights_path)
            return None

    # ── public setup ─────────────────────────────────────────────────────
    def setup(self):
        import torch

        requested_device = getattr(settings, "ML_DEVICE", "cpu")
        if requested_device == "cuda" and not torch.cuda.is_available():
            logger.warning("ML_DEVICE=cuda requested but no GPU is available; falling back to CPU.")
            requested_device = "cpu"
        self.device = torch.device(requested_device)

        models_dir = Path(settings.ML_MODELS_DIR)
        logger.info("━━━━ PakAgri ML Registry — Loading from: %s ━━━━", models_dir)

        if not models_dir.exists():
            logger.error(
                "ML_MODELS_DIR does not exist: %s — verify your .env ML_MODELS_DIR setting.",
                models_dir,
            )

        # ── crop classifier ──────────────────────────────────────────────
        cls_dir = models_dir / "classification"
        classes = self._read_classes_json(cls_dir / "eval_metrics.json")
        self.crop_classes = classes or ["Mango", "Onion", "Sugarcane"]
        self.crop_classifier = self._load_effnet(
            cls_dir / "effnet_b0_best.pth", num_classes=len(self.crop_classes)
        )

        if self.crop_classifier is None:
            logger.error(
                "✗ Crop classifier failed to load — expected: %s/classification/effnet_b0_best.pth",
                models_dir,
            )
        else:
            logger.info("✓ Crop classifier ready. Classes: %s", self.crop_classes)

        # ── per-crop disease models ──────────────────────────────────────
        disease_dir = models_dir / "disease"
        loaded_count = 0
        for crop in ["Mango", "Onion", "Sugarcane"]:
            tag = crop.lower()
            disease_classes = self._read_classes_json(disease_dir / f"{tag}_eval_summary.json")

            effnet_model = None
            if disease_classes:
                effnet_model = self._load_effnet(
                    disease_dir / f"{tag}_effnet_b0_best.pth", num_classes=len(disease_classes)
                )

            yolo_model = self._load_yolo(disease_dir / f"yolov8s_cls_{tag}" / "weights" / "best.pt")

            # If the JSON class list is missing but YOLO loaded fine, YOLO carries its
            # own class names — use those as the source of truth instead.
            if not disease_classes and yolo_model is not None:
                disease_classes = [yolo_model.names[i] for i in range(len(yolo_model.names))]

            self.disease_models[crop] = DiseaseModelSet(
                crop_name=crop,
                classes=disease_classes or [],
                effnet_model=effnet_model,
                yolo_model=yolo_model,
            )

            if self.disease_models[crop].is_available:
                loaded_count += 1
                models_info = []
                if effnet_model:
                    models_info.append("EfficientNet-B0")
                if yolo_model:
                    models_info.append("YOLOv8s-cls")
                logger.info(
                    "✓ %s disease model(s) ready: [%s] — %d classes",
                    crop, " + ".join(models_info), len(disease_classes or [])
                )
            else:
                logger.warning(
                    "✗ No disease model loaded for %s — check %s/disease/%s_*.pth and yolov8s_cls_%s/",
                    crop, models_dir, tag, tag,
                )

        logger.info(
            "━━━━ ML Registry Ready: crop_classifier=%s, disease_models=%d/3 loaded ━━━━",
            "OK" if self.crop_classifier else "FAILED",
            loaded_count,
        )


def get_registry() -> ModelRegistry:
    """Thread-safe lazy singleton — models load once, on first use."""
    global _registry
    if _registry is None:
        with _lock:
            if _registry is None:
                reg = ModelRegistry()
                reg.setup()
                _registry = reg
    return _registry
