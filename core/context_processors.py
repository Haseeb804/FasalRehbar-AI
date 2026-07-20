from django.conf import settings


def site_settings(request):
    return {
        "SITE_NAME": getattr(settings, "SITE_NAME", "PakAgri"),
        "DEFAULT_FROM_EMAIL": settings.DEFAULT_FROM_EMAIL,
    }
