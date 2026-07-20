"""
Inference functions used by detection/services.py.

Pipeline:
  Stage 1 — Crop Classification:  EfficientNet-B0 only  (Mango / Onion / Sugarcane)
  Stage 2 — Disease Detection:    YOLOv8s-cls only       (per-crop disease class)
  Stage 3 — Recommendations:      RAG + OpenAI           (handled in recommendation/rag.py)

Design note: the project trained two model families for disease detection.
Per the product decision, YOLOv8 is the primary disease detector and EfficientNet
is kept loaded only to support the Grad-CAM visualisation (gradcam.py needs the
EfficientNet conv layers). No ensemble averaging is performed for the prediction
that is returned to the user.
"""
import logging
import os
import tempfile

import torch
import torch.nn.functional as F
from PIL import Image as PILImage

from .registry import get_registry
from .transforms import load_image_tensor

logger = logging.getLogger("pakagri.ml")

HEALTHY_LABELS = {"healthy", "healthy leaves"}  # case-insensitive match against class names

# Extensions that YOLOv8's internal data-loader accepts.
# Any other extension (e.g. .jfif) must be converted to .jpg first.
_YOLO_SAFE_EXTS = {"jpg", "jpeg", "png", "bmp", "tif", "tiff", "webp"}


def _is_healthy_label(label: str) -> bool:
    return label.strip().lower() in HEALTHY_LABELS


def _yolo_safe_path(image_path: str):
    """
    Returns (path_to_use, tmp_file_or_None).

    If the original extension is not in YOLO's whitelist, the image is
    re-saved as a temporary JPEG and that temp path is returned.
    The caller is responsible for deleting the temp file when finished.
    """
    ext = image_path.rsplit(".", 1)[-1].lower()
    if ext in _YOLO_SAFE_EXTS:
        return image_path, None

    try:
        img = PILImage.open(image_path).convert("RGB")
        tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
        img.save(tmp.name, format="JPEG", quality=95)
        tmp.close()
        logger.debug("Converted %s -> temp .jpg for YOLO inference", image_path)
        return tmp.name, tmp.name
    except Exception:
        logger.exception("Failed to convert image for YOLO; will try original path")
        return image_path, None


# ─────────────────────────────────────────────────────────
#  Stage 1: Crop Classification  (EfficientNet-B0)
# ─────────────────────────────────────────────────────────

def predict_crop(image_path: str):
    """
    Returns (crop_name: str, confidence: float) or (None, 0.0).

    Uses EfficientNet-B0 only — single model, simple softmax classification
    over the three crop classes [Mango, Onion, Sugarcane].
    """
    registry = get_registry()
    if registry.crop_classifier is None:
        logger.warning("predict_crop called but no crop classifier is loaded.")
        return None, 0.0

    _, tensor = load_image_tensor(image_path, registry.device)
    with torch.no_grad():
        probs = F.softmax(registry.crop_classifier(tensor), dim=1).cpu().numpy()[0]

    idx = int(probs.argmax())
    crop_name = registry.crop_classes[idx]
    confidence = float(probs[idx])
    logger.info("Crop classified as '%s' (%.1f%%)", crop_name, confidence * 100)
    return crop_name, confidence


# ─────────────────────────────────────────────────────────
#  Stage 2: Disease Detection  (YOLOv8s-cls)
# ─────────────────────────────────────────────────────────

def predict_disease(image_path: str, crop_name: str) -> dict:
    """
    Runs the per-crop YOLOv8s-cls disease detector.

    EfficientNet-B0 is NOT used for the final prediction; its weights are
    kept in the registry solely so that Grad-CAM can use the conv layers
    for the visualisation overlay.

    Returns:
        {
            "disease_label":       str | None,   # raw training class name, None if healthy
            "confidence":          float,
            "is_healthy":          bool,
            "is_uncertain":        False,         # always False — single model, no disagreement
            "effnet_label":        "",            # reserved for Grad-CAM
            "effnet_confidence":   0.0,
            "yolo_label":          str,
            "yolo_confidence":     float,
            "all_probs":           dict | None,
        }
    """
    registry = get_registry()
    model_set = registry.disease_models.get(crop_name)

    result = {
        "disease_label": None,
        "confidence": 0.0,
        "is_healthy": True,
        "is_uncertain": False,      # single model — no disagreement possible
        "effnet_label": "",
        "effnet_confidence": 0.0,
        "yolo_label": "",
        "yolo_confidence": 0.0,
        "all_probs": None,
    }

    if model_set is None or not model_set.is_available or not model_set.classes:
        logger.warning("predict_disease: no usable model for crop=%s", crop_name)
        return result

    classes = model_set.classes

    # ── YOLOv8 inference (primary detector) ─────────────────────────────
    yolo_probs = None
    if model_set.has_yolo:
        safe_path, tmp_path = _yolo_safe_path(image_path)
        try:
            yolo_result = model_set.yolo_model.predict(safe_path, verbose=False)[0]
            yolo_probs = yolo_result.probs.data.cpu().numpy()

            # Verify YOLO's own class ordering matches the recorded training order.
            yolo_names = [model_set.yolo_model.names[i] for i in range(len(model_set.yolo_model.names))]
            if yolo_names != classes:
                logger.warning(
                    "Class order mismatch for %s: YOLO=%s vs recorded=%s — "
                    "using YOLO's own class order for this request.",
                    crop_name, yolo_names, classes,
                )
                # Re-map using YOLO's own names as the truth
                classes = yolo_names

        except Exception:
            logger.exception("YOLOv8 inference failed for crop=%s, image=%s", crop_name, image_path)
            yolo_probs = None
        finally:
            if tmp_path:
                try:
                    os.unlink(tmp_path)
                except OSError:
                    pass
    else:
        logger.warning(
            "No YOLOv8 model available for crop=%s — disease detection skipped.", crop_name
        )

    if yolo_probs is None:
        logger.error("Disease detection failed: YOLO returned no result for crop=%s", crop_name)
        return result

    # ── Extract top prediction ───────────────────────────────────────────
    yolo_idx = int(yolo_probs.argmax())
    top_label = classes[yolo_idx]
    top_conf = float(yolo_probs[yolo_idx])

    result["yolo_label"] = top_label
    result["yolo_confidence"] = top_conf
    result["all_probs"] = {cls: float(p) for cls, p in zip(classes, yolo_probs)}
    result["is_healthy"] = _is_healthy_label(top_label)
    result["confidence"] = top_conf
    result["disease_label"] = None if result["is_healthy"] else top_label

    logger.info(
        "Disease detected for %s: '%s' (%.1f%%) | healthy=%s",
        crop_name, top_label, top_conf * 100, result["is_healthy"],
    )
    return result
