from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import ScanImage

# All MIME types that Pillow can open and that we accept for ML inference.
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

CROP_TYPE_CHOICES = [
    ("auto", _("🤖 Auto-Detect Crop (AI Recommended)")),
    ("Onion", _("🧅 Onion (پیاز)")),
    ("Mango", _("🥭 Mango (آم)")),
    ("Sugarcane", _("🌱 Sugarcane (گنا)")),
]


class ImageUploadForm(forms.ModelForm):
    """Form for uploading scan images for plant disease detection."""

    crop_type = forms.ChoiceField(
        choices=CROP_TYPE_CHOICES,
        required=False,
        initial="auto",
        label=_("Target Crop"),
        widget=forms.Select(attrs={
            "class": "form-select fw-semibold py-2 px-3 border-emerald-200",
            "id": "id_crop_type",
        })
    )

    class Meta:
        model = ScanImage
        fields = ["image"]
        widgets = {
            "image": forms.FileInput(attrs={
                "class": "form-control",
                "accept": "image/*",
                "id": "id_image",
                "style": "display: none;",
            })
        }

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image:
            if image.size > 10 * 1024 * 1024:  # 10 MB limit
                raise ValidationError("Image file must not exceed 10 MB.")
            content_type = getattr(image, "content_type", "") or ""
            if content_type and content_type not in ALLOWED_MIME_TYPES:
                raise ValidationError(
                    f"Unsupported image format ({content_type}). "
                    f"Please upload a {ALLOWED_EXTENSIONS_DISPLAY} file."
                )
        return image
