from __future__ import annotations

import os

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F403

DEBUG = os.environ.get("DEBUG", "False").lower() in ("true", "1", "yes")

_prod_hosts_raw = os.environ.get("ALLOWED_HOSTS", "").strip()

if DEBUG:
    ALLOWED_HOSTS = ["*"]
else:
    if not _prod_hosts_raw:
        raise ImproperlyConfigured("ALLOWED_HOSTS required in production")
    ALLOWED_HOSTS = [h.strip() for h in _prod_hosts_raw.split(",") if h.strip()]

postgres_db = os.environ.get("POSTGRES_DB")
postgres_user = os.environ.get("POSTGRES_USER")
postgres_password = os.environ.get("POSTGRES_PASSWORD")
postgres_host = os.environ.get("POSTGRES_HOST", "localhost")
postgres_port = os.environ.get("POSTGRES_PORT", "5432")

if not all((postgres_db, postgres_user, postgres_password)):
    raise ImproperlyConfigured(
        "PostgreSQL: set POSTGRES_DB, POSTGRES_USER, and POSTGRES_PASSWORD."
    )

if SECRET_KEY in (  # noqa: F405
    "",
    None,
    "change-me-in-production-use-long-random-string",
    "dev-only-insecure-key-change-me",
):
    raise ImproperlyConfigured("Set a secure SECRET_KEY in the environment.")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": postgres_db,
        "USER": postgres_user,
        "PASSWORD": postgres_password,
        "HOST": postgres_host,
        "PORT": postgres_port,
        "CONN_MAX_AGE": int(os.environ.get("DB_CONN_MAX_AGE", "60")),
        "OPTIONS": {
            "connect_timeout": 10,
        },
    },
}

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Для локальной разработки отключаем HTTPS требования
if DEBUG:
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
else:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"

_csrf_origins_raw = os.environ.get("CSRF_TRUSTED_ORIGINS", "").strip()

if DEBUG:
    CSRF_TRUSTED_ORIGINS = []
else:
    if not _csrf_origins_raw:
        raise ImproperlyConfigured("CSRF_TRUSTED_ORIGINS required in production")
    CSRF_TRUSTED_ORIGINS = [
        o.strip() for o in _csrf_origins_raw.split(",") if o.strip()
    ]
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
