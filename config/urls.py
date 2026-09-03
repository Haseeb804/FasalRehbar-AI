from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core.views import set_language_view

# Non-translatable/API paths (kept outside i18n_patterns so the API prefix
# never gets a /en/ or /ur/ prefix)
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("set-language/", set_language_view, name="set_language_custom"),
    path("i18n/", include("django.conf.urls.i18n")),  # powers standard language switcher
]

from django.conf.urls.i18n import i18n_patterns  # noqa: E402

urlpatterns += i18n_patterns(
    path("", include("core.urls")),
    path("accounts/", include("accounts.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("detection/", include("detection.urls")),
    path("history/", include("history.urls")),
    path("recommendations/", include("recommendation.urls")),
    prefix_default_language=False,  # English stays at "/", Urdu at "/ur/"
)

handler404 = "core.views.custom_404"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
