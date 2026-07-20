from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent
env = environ.Env(
    DEBUG=(bool, False),
    DJANGO_SECRET_KEY=(str, "django-insecure-change-me"),
    DJANGO_ALLOWED_HOSTS=(list, ["127.0.0.1", "localhost"]),
)

if (BASE_DIR / ".env").exists():
    environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env.bool("DJANGO_DEBUG", default=False)
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["127.0.0.1", "localhost"])

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_filters",
    "accounts",
    "core",
    "dashboard",
    "detection",
    "history",
    "recommendation",
    "api",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",  # enables EN/UR language switching
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
                "core.context_processors.site_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": env.db_url(default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}")
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ── Bilingual support (English / Urdu) ─────────────────────────────────────
LANGUAGES = [
    ("en", "English"),
    ("ur", "اردو"),
]
LOCALE_PATHS = [BASE_DIR / "locale"]

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "auth.User"

LOGIN_URL = "account_login"
LOGIN_REDIRECT_URL = "dashboard:index"
LOGOUT_REDIRECT_URL = "home"

EMAIL_BACKEND = env("EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="no-reply@pakagri.local")

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticatedOrReadOnly"],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# ── ML model weights ────────────────────────────────────────────────────────
# Place the checkpoints trained in the KisanBid Colab notebooks here. See
# ml_models/README.md for the exact expected file layout and names.
ML_MODELS_DIR = env("ML_MODELS_DIR", default=str(BASE_DIR / "ml_models"))
ML_DEVICE = env("ML_DEVICE", default="cpu")  # "cpu" or "cuda" if a GPU is available on the server
ML_IMG_SIZE = env.int("ML_IMG_SIZE", default=224)
# When both EfficientNet-B0 and YOLOv8s-cls top predictions disagree, the
# result is flagged "uncertain" to the farmer instead of silently averaging.
ML_ENSEMBLE_EFFNET_WEIGHT = env.float("ML_ENSEMBLE_EFFNET_WEIGHT", default=0.5)
ML_ENSEMBLE_YOLO_WEIGHT = env.float("ML_ENSEMBLE_YOLO_WEIGHT", default=0.5)

# ── RAG recommendation engine (OpenAI / OpenRouter) ────────────────────────
OPENAI_API_KEY = env("OPENAI_API_KEY", default="")
OPENAI_BASE_URL = env("OPENAI_BASE_URL", default="")  # Set to https://openrouter.ai/api/v1 for OpenRouter
OPENAI_MODEL = env("OPENAI_MODEL", default="gpt-4o-mini")
# If no API key is configured, the app gracefully falls back to showing the
# structured knowledge-base fields directly (no recommendations are ever lost).
RAG_ENABLED = bool(OPENAI_API_KEY)

# ── CrewAI multi-agent pipeline (optional alternative to the direct pipeline) ──
# When True, detection/services.get_detection_service() returns CrewDetectionService
# (3 agents: classification -> detection -> recommendation) instead of the direct,
# non-agentic DetectionService. See detection/crew_service.py for the tradeoffs.
USE_CREWAI_PIPELINE = env.bool("USE_CREWAI_PIPELINE", default=False)
CREWAI_LLM_MODEL = env("CREWAI_LLM_MODEL", default="gpt-4o-mini")

