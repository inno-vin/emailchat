"""
Django settings for backend project (cloud-ready, single instance; no Redis required).
"""

from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------------------------
# Core security / deployment
# ------------------------------------------------------------------------------
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# In production, set SECRET_KEY via env
SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-please-change")

# Comma-separated list in env; example:
# ALLOWED_HOSTS="your-app.onrender.com,yourdomain.com"
ALLOWED_HOSTS = [
    h.strip() for h in os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",") if h.strip()
]

# Needed behind reverse proxies (Render/Railway/etc.)
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# CSRF / CORS
CSRF_TRUSTED_ORIGINS = [
    o.strip() for o in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",") if o.strip()
]
CORS_ALLOWED_ORIGINS = [
    o.strip() for o in os.getenv("CORS_ALLOWED_ORIGINS", "").split(",") if o.strip()
]
CORS_ALLOW_ALL_ORIGINS = not CORS_ALLOWED_ORIGINS  # allow all only if none provided

# ------------------------------------------------------------------------------
# Apps
# ------------------------------------------------------------------------------
INSTALLED_APPS = [
    # Whitenoise helper (avoid Django's dev static during runserver)
    "whitenoise.runserver_nostatic",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "corsheaders",
    "channels",

    # Local apps
    "chat",

    "rest_framework.authtoken",
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

# ------------------------------------------------------------------------------
# ASGI / Channels
# ------------------------------------------------------------------------------
ASGI_APPLICATION = "backend.asgi.application"
WSGI_APPLICATION = "backend.wsgi.application"

# Single-instance websockets (no Redis). If you later need horizontal scaling,
# switch to channels-postgres or an external Redis and update this.
CHANNEL_LAYERS = {
    "default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}
}

# ------------------------------------------------------------------------------
# Middleware
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # must be first
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # serve static on host
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # so TemplateView can find chat.html (optional)
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ------------------------------------------------------------------------------
# Database (DATABASE_URL required in prod; sqlite fallback for quick dev)
# ------------------------------------------------------------------------------
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        ssl_require=not DEBUG,
    )
}

# ------------------------------------------------------------------------------
# Password validation
# ------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ------------------------------------------------------------------------------
# I18N
# ------------------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ------------------------------------------------------------------------------
# Static files
# ------------------------------------------------------------------------------
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ------------------------------------------------------------------------------
# Email (SMTP in prod; console in dev)
# ------------------------------------------------------------------------------
if os.getenv("EMAIL_HOST"):
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = os.getenv("EMAIL_HOST")
    EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
    EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "1") == "1"
    DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "no-reply@example.com")
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    DEFAULT_FROM_EMAIL = "no-reply@example.com"

# ------------------------------------------------------------------------------
# Defaults
# ------------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
