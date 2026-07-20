from django.contrib import admin
from .models import ScanImage, Prediction


@admin.register(ScanImage)
class ScanImageAdmin(admin.ModelAdmin):
    list_display = ("user", "uploaded_at", "is_processed")
    list_filter = ("uploaded_at", "is_processed", "user")
    search_fields = ("user__username",)
    readonly_fields = ("uploaded_at", "image")
    fieldsets = (
        ("Information", {
            "fields": ("user", "image")
        }),
        ("Status", {
            "fields": ("is_processed", "uploaded_at")
        }),
    )


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ("scan_image", "crop", "disease", "confidence_level", "is_healthy", "is_uncertain", "predicted_at")
    list_filter = ("confidence_level", "is_healthy", "is_uncertain", "predicted_at", "crop")
    search_fields = ("scan_image__user__username", "disease__name", "crop__name")
    readonly_fields = ("scan_image", "predicted_at", "processing_time")
    fieldsets = (
        ("Image and Detection", {
            "fields": ("scan_image", "crop", "disease")
        }),
        ("Results", {
            "fields": ("confidence_score", "confidence_level", "is_healthy")
        }),
        ("Model agreement (EfficientNet vs YOLOv8s-cls)", {
            "fields": ("is_uncertain", "effnet_top_label", "effnet_top_confidence",
                       "yolo_top_label", "yolo_top_confidence"),
        }),
        ("Visual diagnosis", {
            "fields": ("analysis_image",),
        }),
        ("Metadata", {
            "fields": ("model_version", "processing_time", "predicted_at")
        }),
    )
