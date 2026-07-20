from django.db import models
from django.contrib.auth.models import User
from detection.models import Prediction


class PredictionHistory(models.Model):
    """Track user prediction history with filtering and search"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="prediction_history")
    prediction = models.OneToOneField(Prediction, on_delete=models.CASCADE)
    
    notes = models.TextField(blank=True)
    tags = models.CharField(max_length=255, blank=True)
    is_archived = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Prediction History"

    def __str__(self):
        return f"{self.user.username} - {self.prediction.predicted_at}"
