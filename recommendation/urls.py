from django.urls import path
from . import views

app_name = "recommendation"

urlpatterns = [
    path("prediction/<int:prediction_id>/", views.recommendation_detail, name="detail"),
    path("<int:recommendation_id>/feedback/", views.submit_feedback, name="feedback"),
]
