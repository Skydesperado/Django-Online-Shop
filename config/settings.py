from pathlib import Path

import dj_database_url
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")

DEBUG = config("DEBUG")

ALLOWED_HOSTS = config("ALLOWED_HOSTS",
                       cast=lambda v: [s.strip() for s in v.split(",")])

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

DATABASES = {"default": dj_database_url.config(default=config("DATABASE_URL"))}

CACHES = {
    "default": {
        "BACKEND": config("BACKEND"),
        "LOCATION": config("LOCATION"),
    }
}

DEFAULT_FILE_STORAGE = config("DEFAULT_FILE_STORAGE")

AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
AWS_S3_ENDPOINT_URL = config("AWS_S3_ENDPOINT_URL")
AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")
AWS_SERVICE_NAME = config("AWS_SERVICE_NAME")
AWS_S3_FILE_OVERWRITE = False
AWS_LOCAL_STORAGE = f"{BASE_DIR}/local/storage/"

CELERY_HOST_NAME = config("CELERY_HOST_NAME")
CELERY_BROKER_URL = config("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND")
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

SESSION_ENGINE = config("SESSION_ENGINE")

DOMAIN = config("DOMAIN", default="127.0.0.1")

DJANGO_ADMIN_URL = config("DJANGO_ADMIN_URL")

BUCKET_URL = config("BUCKET_URL")
BUCKET_DELETE_URL = config("BUCKET_DELETE_URL")
BUCKET_DOWNLOAD_URL = config("BUCKET_DOWNLOAD_URL")

GHASEDAK_API_KEY = config("GHASEDAK_API_KEY")

SANDBOX = config("SANDBOX")

MERCHANT = config("MERCHANT")

CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "full",
    }
}

LANGUAGE_CODE = "en-us"

TIME_ZONE = config("TIME_ZONE")

USE_I18N = True

USE_TZ = True

STATIC_URL = config("STATIC_URL")

STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = config("MEDIA_URL")

MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
