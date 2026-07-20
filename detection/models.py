from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from core.models import Disease, Crop


class ScanImage(models.Model):
    """Store uploaded images for disease detection"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="scan_images")
    image = models.ImageField(
        upload_to="scans/%Y/%m/%d/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "jfif", "png", "webp"]
            )
        ],
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"{self.user.username} - {self.uploaded_at}"


class Prediction(models.Model):
    """Store disease predictions for scanned images"""
    CONFIDENCE_CHOICES = [
        ("high", "High"),
        ("medium", "Medium"),
        ("low", "Low"),
    ]

    scan_image = models.OneToOneField(ScanImage, on_delete=models.CASCADE, related_name="prediction")
    crop = models.ForeignKey(Crop, on_delete=models.SET_NULL, null=True)
    disease = models.ForeignKey(Disease, on_delete=models.SET_NULL, null=True, blank=True)
    confidence_score = models.FloatField(default=0.0)
    confidence_level = models.CharField(max_length=10, choices=CONFIDENCE_CHOICES, default="low")
    is_healthy = models.BooleanField(default=False)
    # True when EfficientNet-B0 and YOLOv8s-cls disagree on the top predicted disease.
    # The UI shows both candidates and a caution message instead of a single falsely-confident answer.
    is_uncertain = models.BooleanField(default=False)
    effnet_top_label = models.CharField(max_length=160, blank=True)
    effnet_top_confidence = models.FloatField(default=0.0)
    yolo_top_label = models.CharField(max_length=160, blank=True)
    yolo_top_confidence = models.FloatField(default=0.0)
    # Grad-CAM heatmap+box overlay showing the model's affected-region focus (not a
    # trained detector's output — see detection/ml/gradcam.py for the caveats).
    analysis_image = models.ImageField(upload_to="scans/analysis/%Y/%m/%d/", blank=True, null=True)
    predicted_at = models.DateTimeField(auto_now_add=True)
    model_version = models.CharField(max_length=50, default="v1.0")
    processing_time = models.FloatField(help_text="Processing time in seconds", default=0.0)

    class Meta:
        ordering = ["-predicted_at"]

    def __str__(self):
        if self.disease:
            return f"{self.scan_image.user.username} - {self.disease.name}"
        return f"{self.scan_image.user.username} - Healthy"

    def get_confidence_percentage(self):
        return round(self.confidence_score * 100, 2)
