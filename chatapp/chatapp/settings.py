import os
from pathlib import Path
import dj_database_url
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret Key (Retrieve from environment variable)
SECRET_KEY = os.getenv("SECRET_KEY", "your-default-secret-key")

# Debug Mode
DEBUG = os.getenv("DEBUG", "False") == "True"

# Allowed Hosts (Use Render domain)
ALLOWED_HOSTS = [os.getenv("RENDER_EXTERNAL_HOSTNAME", "*")]

# Installed Apps
INSTALLED_APPS = [
    "daphne",
    "chat",
    "channels",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "whitenoise.runserver_nostatic",  # Add WhiteNoise for static files
]

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # For serving static files
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "chatapp.urls"

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
            ],
        },
    },
]

# Database Configuration (Use PostgreSQL in Render, SQLite for local development)
if os.getenv("DATABASE_URL"):
    
    DATABASES = {
        "default": dj_database_url.config(default=os.getenv("DATABASE_URL", "sqlite:///db.sqlite3"), conn_max_age=600)
}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Password Validators
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static Files
STATIC_URL = "chat/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "chatapp", "static")]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media Files (If needed)
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# ASGI Application
ASGI_APPLICATION = "chatapp.asgi.application"

# Django Channels Layer (Use Redis in production, In-Memory for local)
USE_REDIS = os.getenv("USE_REDIS", "False") == "True"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer" if USE_REDIS else "channels.layers.InMemoryChannelLayer",
        "CONFIG": {
            "hosts": [os.getenv("REDIS_URL", "redis://localhost:6379")],
        } if USE_REDIS else {},
    },
}

# Login & Logout Redirects
LOGIN_REDIRECT_URL = "/chat/"
LOGOUT_REDIRECT_URL = "/login/"



# Security Settings (For Production)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "False") == "True"
SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "False") == "True"
CSRF_COOKIE_SECURE = os.getenv("CSRF_COOKIE_SECURE", "False") == "True"