from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField(max_length=32, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="profiles/", blank=True, null=True)
    location = models.CharField(max_length=120, blank=True)
    farm_name = models.CharField(max_length=120, blank=True)
    preferred_language = models.CharField(max_length=32, default="en")
    email_verified = models.BooleanField(default=False)
    last_seen = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["user__username"]

    def __str__(self) -> str:
        return f"Profile({self.user.username})"
