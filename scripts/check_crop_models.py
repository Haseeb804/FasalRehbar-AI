import os
import sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
import django
django.setup()
import torch
import torch.nn.functional as F
from detection.models import Prediction

from detection.ml.transforms import val_transform, load_image_tensor
from detection.ml.registry import get_registry

reg = get_registry()

# Check saved_models vs ml_models
paths = [
    os.path.join(base_dir, "saved_models", "classification", "effnet_b0_best.pth"),
    os.path.join(base_dir, "ml_models", "classification", "effnet_b0_best.pth"),
]

for p in paths:
    if os.path.exists(p):
        ckpt = torch.load(p, map_location="cpu", weights_only=False)
        print(f"Path: {p}")
        print(f"  Keys: {list(ckpt.keys()) if isinstance(ckpt, dict) else 'direct model'}")
        if isinstance(ckpt, dict) and "classes" in ckpt:
            print(f"  Classes in ckpt: {ckpt['classes']}")
        if isinstance(ckpt, dict) and "epoch" in ckpt:
            print(f"  Epoch: {ckpt.get('epoch')}, Best Acc: {ckpt.get('best_acc') or ckpt.get('val_acc')}")

# Test predictions on all images in static/images and media/scans
test_images = [
    os.path.join(base_dir, "static", "images", "onion_showcase.jpg"),
    os.path.join(base_dir, "static", "images", "mango_showcase.jpg"),
    os.path.join(base_dir, "static", "images", "hero_agri_bg.jpg"),
]

for p in Prediction.objects.order_by('-id')[:5]:
    if p.scan_image and p.scan_image.image:
        test_images.append(p.scan_image.image.path)

print("\n=== TESTING CROP CLASSIFICATION ACROSS TEST IMAGES ===")
for img_path in set(test_images):
    if not os.path.exists(img_path):
        continue
    _, tensor = load_image_tensor(img_path, "cpu")
    with torch.no_grad():
        logits = reg.crop_classifier(tensor)
        probs = F.softmax(logits, dim=1).cpu().numpy()[0]
    
    print(f"\nImage: {os.path.basename(img_path)}")
    for c_name, pr in zip(reg.crop_classes, probs):
        print(f"   {c_name:10}: {pr*100:6.2f}% (logit: {float(logits[0][reg.crop_classes.index(c_name)]):.3f})")
