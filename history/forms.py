from django import forms
from .models import PredictionHistory


class PredictionHistoryForm(forms.ModelForm):
    """Form for managing prediction history"""
    
    class Meta:
        model = PredictionHistory
        fields = ["notes", "tags"]
        widgets = {
            "notes": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Add notes about this prediction..."
            }),
            "tags": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Add tags separated by commas (e.g., urgent, follow-up)"
            })
        }


class PredictionFilterForm(forms.Form):
    """Form for filtering prediction history"""
    DISEASE_CHOICES = [("", "All Diseases")]
    CROP_CHOICES = [("", "All Crops")]
    CONFIDENCE_CHOICES = [
        ("", "All Confidence Levels"),
        ("high", "High"),
        ("medium", "Medium"),
        ("low", "Low"),
    ]

    disease = forms.ChoiceField(
        choices=DISEASE_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "form-select"})
    )
    crop = forms.ChoiceField(
        choices=CROP_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "form-select"})
    )
    confidence = forms.ChoiceField(
        choices=CONFIDENCE_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "form-select"})
    )
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Search by tags or notes..."
        })
    )
