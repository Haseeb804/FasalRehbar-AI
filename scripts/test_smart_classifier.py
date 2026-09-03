import os
import sys
import torch
import torch.nn.functional as F

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
import django
django.setup()

from detection.ml.registry import get_registry
from detection.ml.transforms import load_image_tensor

reg = get_registry()

def smart_predict_crop(image_path: str):
    registry = get_registry()
    if registry.crop_classifier is None:
        return None, 0.0

    _, tensor = load_image_tensor(image_path, registry.device)
    with torch.no_grad():
        probs = F.softmax(registry.crop_classifier(tensor), dim=1).cpu().numpy()[0]

    top_idx = int(probs.argmax())
    top_crop = registry.crop_classes[top_idx]
    top_conf = float(probs[top_idx])

    # If decisive confidence, return immediately
    if top_conf >= 0.85:
        return top_crop, top_conf

    # Disambiguation: test candidate crops with YOLO disease models
    print(f"  [Disambiguation Triggered] Initial top crop: {top_crop} ({top_conf*100:.1f}%)")
    best_crop = top_crop
    best_score = top_conf

    for idx, crop in enumerate(registry.crop_classes):
        crop_prob = float(probs[idx])
        if crop_prob < 0.05:  # skip highly improbable crops
            continue

        mset = registry.disease_models.get(crop)
        yolo_conf = 0.0
        if mset and mset.yolo_model:
            try:
                yolo_res = mset.yolo_model.predict(source=image_path, verbose=False)[0]
                yolo_conf = float(yolo_res.probs.top1conf)
                yolo_label = yolo_res.names[yolo_res.probs.top1]
                print(f"    Evaluating candidate {crop:9}: CropProb={crop_prob*100:.1f}%, YOLO={yolo_label} ({yolo_conf*100:.1f}%)")
            except Exception as e:
                print(f"    YOLO error for {crop}: {e}")

        # Combined score: 60% crop prior + 40% disease fit
        joint_score = 0.6 * crop_prob + 0.4 * yolo_conf
        if joint_score > best_score:
            best_score = joint_score
            best_crop = crop

    print(f"  -> Selected Crop after Disambiguation: {best_crop} (joint score: {best_score:.3f})")
    return best_crop, top_conf

test_imgs = [
    os.path.join(base_dir, "media", "scans", "2026", "09", "03", "eric_stigmina2a.png"),
    os.path.join(base_dir, "static", "images", "onion_showcase.jpg"),
    os.path.join(base_dir, "media", "scans", "2026", "07", "22", "360_F_523372476_5eh9JBDnhsuvHreuM5eiGlnjsbq6Nf0J.jpg"),
]

for img in test_imgs:
    if os.path.exists(img):
        print(f"\n--- Testing {os.path.basename(img)} ---")
        smart_predict_crop(img)
