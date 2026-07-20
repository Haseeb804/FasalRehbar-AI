from django import forms

from .models import ContactMessage, Feedback


class StyledFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"form-control rounded-4 shadow-sm {classes}".strip()


class ContactForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ("name", "email", "subject", "message")
        widgets = {"message": forms.Textarea(attrs={"rows": 5})}


class FeedbackForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ("name", "email", "rating", "subject", "message")
        widgets = {"message": forms.Textarea(attrs={"rows": 5})}
