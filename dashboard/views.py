from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages

from accounts.models import Profile
from accounts.forms import ProfileUpdateForm
from history.models import PredictionHistory
from detection.models import Prediction


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get prediction stats
        predictions = Prediction.objects.filter(scan_image__user=user)
        healthy_count = predictions.filter(is_healthy=True).count()
        disease_count = predictions.exclude(disease__isnull=True).count()
        high_confidence_count = predictions.filter(confidence_level="high").count()
        
        onion_count = predictions.filter(crop__name__iexact="Onion").count()
        mango_count = predictions.filter(crop__name__iexact="Mango").count()
        sugarcane_count = predictions.filter(crop__name__iexact="Sugarcane").count()

        context.update(
            {
                "total_scans": predictions.count(),
                "healthy_count": healthy_count,
                "disease_count": disease_count,
                "high_confidence_count": high_confidence_count,
                "onion_count": onion_count,
                "mango_count": mango_count,
                "sugarcane_count": sugarcane_count,
                "recent_scans": predictions.order_by("-predicted_at")[:8],
                "profile": getattr(user, "profile", None),
            }
        )
        return context


class ProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = "dashboard/profile.html"
    success_url = reverse_lazy("dashboard:profile")

    def get_object(self, queryset=None):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def form_valid(self, form):
        messages.success(self.request, "Profile updated successfully.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Profile"
        return context


class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/settings.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Settings"
        return context
