"""
Utility functions for image processing and validation.
"""

import os
from PIL import Image
from django.core.files.storage import default_storage


def validate_image_file(image):
    """Validate image file"""
    allowed_extensions = ["jpg", "jpeg", "png"]
    max_size = 5 * 1024 * 1024  # 5MB

    if image.size > max_size:
        return False, "Image size exceeds 5MB limit"

    file_name = image.name.lower()
    if not any(file_name.endswith(ext) for ext in allowed_extensions):
        return False, "Only JPG, JPEG, and PNG formats are allowed"

    return True, "Image is valid"


def resize_image(image_path, width=800, height=600):
    """Resize image to specified dimensions"""
    try:
        image = Image.open(image_path)
        image.thumbnail((width, height), Image.Resampling.LANCZOS)
        image.save(image_path)
        return True
    except Exception as e:
        print(f"Error resizing image: {str(e)}")
        return False


def crop_image_center(image_path, size=600):
    """Crop image to center square"""
    try:
        image = Image.open(image_path)
        width, height = image.size

        if width > size or height > size:
            left = (width - size) // 2
            top = (height - size) // 2
            right = left + size
            bottom = top + size

            image = image.crop((left, top, right, bottom))
            image.save(image_path)

        return True
    except Exception as e:
        print(f"Error cropping image: {str(e)}")
        return False
