from django.conf import settings

IMMUNITY_CONTROLLER_API_HOST = getattr(settings, 'IMMUNITY_CONTROLLER_API_HOST', None)
