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


def set_language_view(request):
    """
    Robust language switcher handling prefix_default_language=False.
    Redirects between /... and /ur/... cleanly while preserving the exact query/path.
    """
    import urllib.parse
    from django.conf import settings
    from django.http import HttpResponseRedirect
    from django.utils import translation

    lang_code = request.POST.get("language") or request.GET.get("language") or "en"
    if lang_code not in ("en", "ur"):
        lang_code = "en"

    translation.activate(lang_code)

    next_url = request.POST.get("next") or request.GET.get("next") or request.META.get("HTTP_REFERER") or "/"
    parsed = urllib.parse.urlparse(next_url)
    path = parsed.path or "/"

    if lang_code == "ur":
        if not path.startswith("/ur/") and path != "/ur":
            path = "/ur" + (path if path.startswith("/") else "/" + path)
    else:  # "en"
        if path.startswith("/ur/"):
            path = path[3:]
        elif path == "/ur":
            path = "/"

    redirect_url = urllib.parse.urlunparse((
        parsed.scheme, parsed.netloc, path, parsed.params, parsed.query, parsed.fragment
    ))

    response = HttpResponseRedirect(redirect_url or "/")
    response.set_cookie(
        settings.LANGUAGE_COOKIE_NAME,
        lang_code,
        max_age=settings.LANGUAGE_COOKIE_AGE,
        path=settings.LANGUAGE_COOKIE_PATH,
        domain=settings.LANGUAGE_COOKIE_DOMAIN,
        secure=settings.LANGUAGE_COOKIE_SECURE,
        httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
        samesite=settings.LANGUAGE_COOKIE_SAMESITE,
    )
    if hasattr(request, "session"):
        session_key = getattr(translation, "LANGUAGE_SESSION_KEY", "_language")
        request.session[session_key] = lang_code
    return response
