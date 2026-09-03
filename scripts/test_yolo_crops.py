import os
import sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
import django
django.setup()

from detection.ml.registry import get_registry

reg = get_registry()

test_images = [
    os.path.join(base_dir, "media", "scans", "2026", "09", "03", "eric_stigmina2a.png"),
    os.path.join(base_dir, "media", "scans", "2026", "07", "22", "360_F_523372476_5eh9JBDnhsuvHreuM5eiGlnjsbq6Nf0J.jpg"),
]

for img in test_images:
    if not os.path.exists(img):
        continue
    print(f"\n==========================================")
    print(f"IMAGE: {os.path.basename(img)}")
    print(f"==========================================")
    
    # 1. Crop classifier
    import torch
    import torch.nn.functional as F
    from detection.ml.transforms import load_image_tensor
    _, tensor = load_image_tensor(img, "cpu")
    with torch.no_grad():
        probs = F.softmax(reg.crop_classifier(tensor), dim=1).cpu().numpy()[0]
    for c, p in zip(reg.crop_classes, probs):
        print(f"  Crop Model -> {c:10}: {p*100:5.2f}%")
        
    # 2. Disease models for each crop
    for crop in ["Mango", "Onion", "Sugarcane"]:
        mset = reg.disease_models.get(crop)
        if mset and mset.yolo_model:
            res = mset.yolo_model.predict(source=img, verbose=False)[0]
            yolo_top_idx = res.probs.top1
            yolo_top_conf = float(res.probs.top1conf)
            yolo_label = res.names[yolo_top_idx]
            print(f"  YOLO [{crop:9}] -> Top: {yolo_label:25} ({yolo_top_conf*100:5.2f}%)")
