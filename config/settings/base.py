try:
    from decouple import config
except ImportError:
    try:
        from python_decouple import config
    except ImportError:
        import os
        def config(name, default=None, cast=None):
            value = os.environ.get(name, default)
            if value is None:
                return None
            if cast == bool:
                return value.lower() in ('true', 't', 'yes', 'y', '1')
            elif cast:
                return cast(value)
            return value

import os
from pathlib import Path

# Set BASE_DIR
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if "DJANGO_BASE_DIR" not in os.environ:
    os.environ["DJANGO_BASE_DIR"] = str(BASE_DIR)

# Set SCRAPER_STORAGE_DIR
if "SCRAPER_STORAGE_DIR" not in os.environ:
    SCRAPER_STORAGE_DIR = os.path.join(BASE_DIR, 'media', 'scraped_data')
    os.environ["SCRAPER_STORAGE_DIR"] = SCRAPER_STORAGE_DIR
else:
    SCRAPER_STORAGE_DIR = os.environ["SCRAPER_STORAGE_DIR"]
SCRAPED_FILES_DIR = 'scraped_data'
# Ensure the storage directory exists
os.makedirs(SCRAPER_STORAGE_DIR, exist_ok=True)

# Environment settings
ENVIRONMENT = config('ENVIRONMENT', default='development').lower()
IS_DEVELOPMENT = ENVIRONMENT == 'development'

# Secret key configuration
SECRET_KEY = config('SECRET_KEY', default=None)
if not SECRET_KEY:
    if not IS_DEVELOPMENT:
        raise ValueError("SECRET_KEY environment variable must be set in production mode")
    SECRET_KEY = 'dev-only-insecure-key-do-not-use-in-production'

# Debug and allowed hosts
DEBUG = config('DEBUG', default='True' if IS_DEVELOPMENT else 'False', cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1' if IS_DEVELOPMENT else '').split(',')

# Storage backend settings
STORAGE_BACKEND = os.environ.get('STORAGE_BACKEND', 'local')
STORAGE_OPTIONS = {
    'local': {
        'ROOT_DIR': os.path.join(BASE_DIR, 'media'),
    },
    's3': {
        'BUCKET': os.environ.get('S3_BUCKET'),
        'ACCESS_KEY': os.environ.get('S3_ACCESS_KEY'),
        'SECRET_KEY': os.environ.get('S3_SECRET_KEY'),
        'REGION': os.environ.get('S3_REGION', 'us-east-1'),
    }
}

# Enabled scrapers configuration
ENABLED_SCRAPERS = {
    'BNB': {
        'module': 'apps.bg_data_scrapers.scrapers.bnb_scraper',
        'class': 'BNBScraper',
        'schedule': '0 0 * * *',  # Daily at midnight
    },
    'NSI': {
        'module': 'apps.bg_data_scrapers.scrapers.nsi_scraper',
        'class': 'NSIScraper',
        'schedule': '0 0 * * 1',  # Weekly on Monday
    }
}

# For admin site optimization
ADMIN_SITE_HEADER = "Data Platform Admin"
ADMIN_SITE_TITLE = "Data Platform"
ADMIN_INDEX_TITLE = "Administration"

# Celery settings
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
]

THIRD_PARTY_APPS = [
    'rest_framework',
]

LOCAL_APPS = [
    'apps.core',
    'apps.bg_data_scrapers',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.gzip.GZipMiddleware',  # Added for compression
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',  # Added for HTTP caching
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'config.urls'

# Required for django-debug-toolbar to work
INTERNAL_IPS = [
    '127.0.0.1',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Added central templates directory
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'postgres'),
        'USER': os.environ.get('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'password'),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
        'CONN_MAX_AGE': 600,  # Keep connections alive for 10 minutes
        'OPTIONS': {
            'connect_timeout': 10,
        },
    }
}

# Cache configuration
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")  # Used for `collectstatic`
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]  # Place where you store static files

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day'
    }
}

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# Import scraper settings safely at the end of the file
# after Django's app registry is fully loaded
try:
    from apps.bg_data_scrapers.scrapers.settings import SCRAPER_SETTINGS
except ImportError:
    SCRAPER_SETTINGS = {}

# Scraper configurations - use values from SCRAPER_SETTINGS where appropriate
SCRAPER_CONFIG = {
    'STORAGE_DIR': SCRAPER_STORAGE_DIR,
    'LOGGING_ENABLED': True,
    'LOGGING_LEVEL': 'INFO',
    'SCRAPER_SETTINGS': SCRAPER_SETTINGS,
}