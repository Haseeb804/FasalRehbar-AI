from django.urls import path

from .views import AboutView, ContactView, FAQView, FeedbackView, HomeView, PrivacyPolicyView, ServicesView, TermsView

app_name = "core"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("services/", ServicesView.as_view(), name="services"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("feedback/", FeedbackView.as_view(), name="feedback"),
    path("faq/", FAQView.as_view(), name="faq"),
    path("privacy-policy/", PrivacyPolicyView.as_view(), name="privacy"),
    path("terms-and-conditions/", TermsView.as_view(), name="terms"),
]
