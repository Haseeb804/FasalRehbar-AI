from django import forms
from .models import UserFeedback


class FeedbackForm(forms.ModelForm):
    """Form for user feedback on recommendations"""
    
    class Meta:
        model = UserFeedback
        fields = ["feedback_type", "rating", "comment"]
        widgets = {
            "feedback_type": forms.RadioSelect(choices=UserFeedback.FEEDBACK_CHOICES),
            "rating": forms.RadioSelect(choices=[(i, f"{'⭐' * i}") for i in range(1, 6)]),
            "comment": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Tell us what you think..."
            })
        }
