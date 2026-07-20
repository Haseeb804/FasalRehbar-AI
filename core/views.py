from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from .forms import ContactForm, FeedbackForm
from .models import Crop, Disease, FAQ


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "crop_count": Crop.objects.filter(is_active=True).count(),
                "disease_count": Disease.objects.filter(is_active=True).count(),
                "faq_count": FAQ.objects.filter(is_active=True).count(),
            }
        )
        return context


class AboutView(TemplateView):
    template_name = "core/about.html"


class ServicesView(TemplateView):
    template_name = "core/services.html"


class FAQView(TemplateView):
    template_name = "core/faq.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q", "")
        faqs = FAQ.objects.filter(is_active=True)
        if query:
            faqs = faqs.filter(Q(question__icontains=query) | Q(answer__icontains=query))
        context["faqs"] = faqs
        context["search_query"] = query
        return context


class PrivacyPolicyView(TemplateView):
    template_name = "core/privacy.html"


class TermsView(TemplateView):
    template_name = "core/terms.html"


class ContactView(FormView):
    template_name = "core/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact")

    def form_valid(self, form):
        form.save()
        from django.contrib import messages

        messages.success(self.request, "Thanks for reaching out. Our team will contact you soon.")
        return super().form_valid(form)


class FeedbackView(FormView):
    template_name = "core/feedback.html"
    form_class = FeedbackForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        feedback = form.save(commit=False)
        if self.request.user.is_authenticated:
            feedback.user = self.request.user
        feedback.save()
        from django.contrib import messages

        messages.success(self.request, "Thank you for your feedback.")
        return super().form_valid(form)


def custom_404(request, exception=None):
    return render(request, "core/404.html", status=404)
