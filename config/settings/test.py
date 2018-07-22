from .base import *

DEBUG = False

AUTHENTICATION_BACKENDS += ('django.contrib.auth.backends.ModelBackend',)
