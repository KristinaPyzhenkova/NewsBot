import os
import dotenv

dotenv.load_dotenv('../../.env')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SECRET_KEY = os.getenv("SECRET_KEY", 'secret')
DEBUG = int(os.getenv("DEBUG", 0))

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1 localhost db web").split(" ")
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
SITE_DOMAIN = os.getenv("SITE_DOMAIN", None)

CSRF_TRUSTED_ORIGINS = [
   'http://127.0.0.1:8000',
   'http://localhost:8000',
] + ([f'https://{SITE_DOMAIN}', f'https://{SITE_DOMAIN}:8443'] if SITE_DOMAIN else [])


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django_celery_beat",
    "django.contrib.staticfiles",
    "telegram_bot"
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "app.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": os.getenv("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.getenv("SQL_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": os.getenv("SQL_USER", "user"),
        "PASSWORD": os.getenv("SQL_PASSWORD", "password"),
        "HOST": os.getenv("SQL_HOST", "localhost"),
        "PORT": os.getenv("SQL_PORT", "5432"),
        'ATOMIC_REQUESTS': True,
    }
}


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

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# CELERY, REDIS
REDIS_URL = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_BROKER_URL = os.getenv('REDIS_HOST')
CELERY_BACKEND_URL = os.getenv('REDIS_HOST')
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = os.getenv('TIMEZONE')
CELERY_RESULT_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = f"{os.getenv('REDIS_HOST')}/0"
CELERY_RESULT_EXPIRES = 60

BROKER_URL = os.getenv('REDIS_HOST')
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}

DATETIME_FORMATTER = '%d/%b/%Y %H:%M:%S'

LOG_FORMATTER = (
    '[%(asctime)s] %(levelname)s: %(funcName)s %(message)s'
)

LOG_FILE = os.path.join('/app/logs', 'app.log')
LOG_FILE_WATCHED = os.path.join('/app/logs', 'watched_file.log')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': LOG_FORMATTER,
            'datefmt': DATETIME_FORMATTER,
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
        'timed_rotating_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': LOG_FILE,
            'formatter': 'console',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 7,
        },
        'watched_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': LOG_FILE_WATCHED,
            'formatter': 'console',
        },
    },
    'loggers': {
        'main': {
            'level': 'DEBUG',
            'handlers': ['console', 'timed_rotating_file', 'watched_file'],
            'propagate': False,
        },
        'console': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}
