from . import settings as app_settings


def controller_api_settings(request):
    return {
        'IMMUNITY_CONTROLLER_API_HOST': app_settings.IMMUNITY_CONTROLLER_API_HOST,
    }
