from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.storage import default_storage
from .models import ScanImage
import os


@receiver(post_save, sender=ScanImage)
def cleanup_old_scan_images(sender, instance, created, **kwargs):
    """
    Optional: Implement cleanup logic for old scan images
    """
    pass
