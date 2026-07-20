from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register(r"diseases", views.DiseaseViewSet, basename="disease")
router.register(r"crops", views.CropViewSet, basename="crop")
router.register(r"predictions", views.PredictionViewSet, basename="prediction")
router.register(r"recommendations", views.RecommendationViewSet, basename="recommendation")

app_name = "api"

urlpatterns = [
    path("", include(router.urls)),
]
