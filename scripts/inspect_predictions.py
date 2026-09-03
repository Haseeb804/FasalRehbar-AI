import os
import sys
import django

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from detection.models import Prediction, ScanImage
from detection.ml.inference import predict_crop, predict_disease
from detection.ml.registry import get_registry

print("=== RECENT PREDICTIONS IN DATABASE ===")
for p in Prediction.objects.order_by('-id')[:10]:
    crop_name = p.crop.name if p.crop else "None"
    disease_name = p.disease.name if p.disease else "Healthy"
    img_path = p.scan_image.image.path if p.scan_image and p.scan_image.image else "No file"
    print(f"ID: {p.id:2} | DB Crop: {crop_name:10} | DB Disease: {disease_name:25} | Conf: {p.confidence_score:.2f} | Img: {img_path}")
    
    if os.path.exists(img_path):
        crop_pred, crop_conf = predict_crop(img_path)
        disease_res = predict_disease(img_path, crop_pred) if crop_pred else {}
        print(f"    -> Re-test inference: Crop: {crop_pred} ({crop_conf*100:.1f}%) | Disease: {disease_res.get('disease_label')} ({disease_res.get('confidence', 0)*100:.1f}%)")
