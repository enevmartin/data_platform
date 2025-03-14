"""
Development settings for the data platform.
"""
from .base import *  # noqa

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'dev-only-insecure-key-do-not-use-in-production'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Allow Django Debug Toolbar
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE.insert(1, 'debug_toolbar.middleware.DebugToolbarMiddleware')
INTERNAL_IPS = ['127.0.0.1']

# Use Django's built-in console email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Cache settings for development (faster flush/refresh cycle)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Log SQL queries in development
LOGGING['loggers'] = {
    'django.db.backends': {
        'level': 'DEBUG',
        'handlers': ['console'],
    }
}

# Disable throttling in development
REST_FRAMEWORK['DEFAULT_THROTTLE_CLASSES'] = []