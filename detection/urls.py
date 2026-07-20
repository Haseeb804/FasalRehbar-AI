from django.urls import path
from . import views

app_name = "detection"

urlpatterns = [
    path("", views.detection_index, name="index"),
    path("upload/", views.upload_image, name="upload"),
    path("result/<int:pk>/", views.detection_result, name="result"),
    path("history/", lambda request: __import__('django.shortcuts', fromlist=['redirect']).redirect('history:list'), name="history"),

    path("prediction/<int:pk>/", views.PredictionDetailView.as_view(), name="prediction_detail"),
]
