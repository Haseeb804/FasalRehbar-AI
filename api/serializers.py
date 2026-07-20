from rest_framework import serializers
from detection.models import ScanImage, Prediction
from core.models import Disease, Crop
from recommendation.models import Recommendation


class DiseaseSerializer(serializers.ModelSerializer):
    crop_name = serializers.CharField(source="crop.name", read_only=True)

    class Meta:
        model = Disease
        fields = ["id", "name", "crop", "crop_name", "description", "symptoms",
                  "causes", "treatment", "prevention", "severity"]


class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = ["id", "name", "scientific_name", "description"]


class ScanImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScanImage
        fields = ["id", "image", "uploaded_at", "is_processed"]


class PredictionSerializer(serializers.ModelSerializer):
    crop_name = serializers.CharField(source="crop.name", read_only=True)
    disease_name = serializers.CharField(source="disease.name", read_only=True)
    confidence_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Prediction
        fields = [
            "id",
            "crop",
            "crop_name",
            "disease",
            "disease_name",
            "confidence_score",
            "confidence_level",
            "confidence_percentage",
            "is_healthy",
            "predicted_at",
            "processing_time",
        ]

    def get_confidence_percentage(self, obj):
        return obj.get_confidence_percentage()


class RecommendationSerializer(serializers.ModelSerializer):
    prediction = PredictionSerializer(read_only=True)

    class Meta:
        model = Recommendation
        fields = [
            "id",
            "prediction",
            "disease",
            "treatment_steps",
            "prevention_steps",
            "urgency",
            "additional_notes",
        ]
