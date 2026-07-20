from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from core.models import Disease, Crop
from detection.models import Prediction
from recommendation.models import Recommendation
from .serializers import (
    DiseaseSerializer,
    CropSerializer,
    PredictionSerializer,
    RecommendationSerializer,
)


class DiseaseViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for diseases"""
    queryset = Disease.objects.filter(is_active=True)
    serializer_class = DiseaseSerializer
    filter_backends = [SearchFilter]
    search_fields = ["name", "description", "symptoms"]


class CropViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for crops"""
    queryset = Crop.objects.filter(is_active=True)
    serializer_class = CropSerializer
    filter_backends = [SearchFilter]
    search_fields = ["name", "scientific_name"]


class PredictionViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for predictions"""
    serializer_class = PredictionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["confidence_level", "is_healthy"]
    ordering_fields = ["predicted_at", "confidence_score"]
    ordering = ["-predicted_at"]

    def get_queryset(self):
        return Prediction.objects.filter(scan_image__user=self.request.user)

    @action(detail=True, methods=["get"])
    def statistics(self, request, pk=None):
        """Get statistics about predictions"""
        predictions = self.get_queryset()
        stats = {
            "total_predictions": predictions.count(),
            "healthy_plants": predictions.filter(is_healthy=True).count(),
            "diseases_detected": predictions.exclude(disease__isnull=True).count(),
            "high_confidence": predictions.filter(confidence_level="high").count(),
        }
        return Response(stats)


class RecommendationViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for recommendations"""
    serializer_class = RecommendationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["urgency"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return Recommendation.objects.filter(
            prediction__scan_image__user=self.request.user
        ).select_related("prediction", "disease")
