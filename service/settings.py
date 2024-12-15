import os
from pathlib import Path

from decouple import config  # type: ignore

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY: str = config(
    "DJANGO_SECRET_KEY", default="django-default-secret key", cast=str  # type: ignore
)

DEBUG: bool = config("DEBUG", default=False, cast=bool)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Apps
    "analysis.apps.AnalysisConfig",
    # Plugins
    "rest_framework",
    "corsheaders",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
        "rest_framework.renderers.AdminRenderer",
    ],
}

ROOT_URLCONF = "service.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR, "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "service.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "db.sqlite3",
    }
}

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": config("DB_NAME", default="postgres", cast=str),
#         "USER": config("DB_USER", default="postgres", cast=str),
#         "PASSWORD": config("DB_PASS", default="postgres", cast=str),
#         "HOST": config("DB_HOST", default="localhost", cast=str),
#         "PORT": config("DB_PORT", default="5432", cast=str),
#     }
# }

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ASGI_APPLICATION = "service.asgi.application"

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://localhost:5173",
    "http://0.0.0.0:5173",
    "http://127.0.0.1:5173",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://localhost:3000",
    "http://0.0.0.0:3000",
    "http://127.0.0.1:3000",
]

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "0.0.0.0",
]

CORS_ALLOW_CREDENTIALS = True
CORS_EXPOSE_HEADERS = ["Authorization"]

CORS_ALLOW_HEADERS = [
    "Cache-Control",
    "Authorization",
    "Content-Type",
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "{asctime} {levelname} {name} {message}",
            "style": "{",
        },
        "verbose": {
            "format": "{levelname} {asctime} {name} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        },
        "file": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": "django.log",
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "DEBUG",
    },
}
