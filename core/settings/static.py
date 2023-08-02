"""
Configuration for collecting static files in production.
Do not use as runtime settings. Server should be running with `core.settings.prod`!
"""
from django.core.management.utils import get_random_secret_key

from core.settings.base import *

ALLOWED_HOSTS = []

SECRET_KEY = get_random_secret_key()

DEBUG = False

MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATIC_URL = '/static/'
