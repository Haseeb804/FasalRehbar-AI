from django import forms
from django.core.exceptions import ValidationError
from .models import ScanImage

# All MIME types that Pillow can open and that we accept for ML inference.
# jfif is a JPEG variant saved by many browsers/phones; webp is increasingly common.
ALLOWED_MIME_TYPES = {
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/webp",
    "image/jfif",           # non-standard but some browsers report this
    "image/pjpeg",          # IE/Edge progressive JPEG
    "image/x-citrix-jpeg",  # Citrix JPEG variant
}

ALLOWED_EXTENSIONS_DISPLAY = "PNG, JPG, JPEG, JFIF, WEBP"


class ImageUploadForm(forms.ModelForm):
    """Form for uploading scan images for plant disease detection."""

    class Meta:
        model = ScanImage
        fields = ["image"]
        widgets = {
            "image": forms.FileInput(attrs={
                "class": "form-control",
                # Keep accept broad — the browser uses this only for the file-picker UI.
                # The real validation is in clean_image() below.
                "accept": "image/*",
                # ID matches the JS getElementById('id_image') calls in detection/index.html
                "id": "id_image",
                "style": "display: none;",  # hidden — users interact with the drop-zone
            })
        }

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image:
            if image.size > 10 * 1024 * 1024:  # 10 MB limit (raised from 5 MB)
                raise ValidationError("Image file must not exceed 10 MB.")
            content_type = getattr(image, "content_type", "") or ""
            if content_type and content_type not in ALLOWED_MIME_TYPES:
                raise ValidationError(
                    f"Unsupported image format ({content_type}). "
                    f"Please upload a {ALLOWED_EXTENSIONS_DISPLAY} file."
                )
        return image

