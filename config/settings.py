import os
from pathlib import Path

import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = os.environ.get("DEBUG")

ALLOWED_HOSTS = ["*"]

LOCAL_APPS = [
    "shop.apps.ShopConfig",
    "users.apps.UsersConfig",
    "zarinpal.apps.ZarinpalConfig",
]

THIRD_PARTY_APPS = [
    "storages",
    "django_celery_beat",
    "ckeditor",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    *LOCAL_APPS,
    *THIRD_PARTY_APPS,
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
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
                "utilities.contextprocessors.cart",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default":
    dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        engine="django.db.backends.postgresql",
    )
}

CACHES = {
    "default": {
        "BACKEND": os.environ.get("BACKEND"),
        "LOCATION": os.environ.get("LOCATION"),
    }
}

DEFAULT_FILE_STORAGE = os.environ.get("DEFAULT_FILE_STORAGE")

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_S3_ENDPOINT_URL = os.environ.get("AWS_S3_ENDPOINT_URL")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_SERVICE_NAME = os.environ.get("AWS_SERVICE_NAME")
AWS_S3_FILE_OVERWRITE = False
AWS_LOCAL_STORAGE = f"{BASE_DIR}/local/storage/"

CELERY_HOST_NAME = os.environ.get("CELERY_HOST_NAME")
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND")
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_BROKER_CONNECTION_RETRY = True
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_BROKER_CONNECTION_MAX_RETRIES = 5

AUTH_USER_MODEL = "users.User"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME":
        "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

SESSION_ENGINE = os.environ.get("SESSION_ENGINE")

DOMAIN = os.environ.get("DOMAIN", default="127.0.0.1")

DJANGO_ADMIN_URL = os.environ.get("DJANGO_ADMIN_URL")

BUCKET_URL = os.environ.get("BUCKET_URL")
BUCKET_DELETE_URL = os.environ.get("BUCKET_DELETE_URL")
BUCKET_DOWNLOAD_URL = os.environ.get("BUCKET_DOWNLOAD_URL")

GHASEDAK_API_KEY = os.environ.get("GHASEDAK_API_KEY")

SANDBOX = os.environ.get("SANDBOX")

MERCHANT = os.environ.get("MERCHANT")

CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "full",
    }
}

LANGUAGE_CODE = "en-us"

TIME_ZONE = os.environ.get("TIME_ZONE")

USE_I18N = True

USE_TZ = True

STATIC_URL = os.environ.get("STATIC_URL")

STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = os.environ.get("MEDIA_URL")

MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
