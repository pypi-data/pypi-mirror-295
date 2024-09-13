from django.conf import settings
from django.urls import include, path

url_metadata = [
    # allauth proxy
    {
        'regexp': 'accounts/',
        'app': 'openwisp_users',
        'include': {'module': 'openwisp_users.accounts.urls'},
    },
    # openwisp_notifications
    {
        'regexp': '',
        'app': 'openwisp_notifications',
        'include': {'module': 'openwisp_notifications.urls'},
    },
    # openwisp_ipam
    {
        'regexp': '',
        'app': 'openwisp_ipam',
        'include': {'module': 'openwisp_ipam.urls'},
    },
    # immunity_controller.pki (CRL view)
    {
        'regexp': '',
        'app': 'immunity_controller.pki',
        'include': {'module': '{app}.urls', 'namespace': 'x509'},
    },
    # immunity_controller.pki.api
    {
        'regexp': 'api/v1/',
        'app': 'immunity_controller.pki',
        'include': {'module': '{app}.api.urls', 'namespace': 'pki_api'},
    },
    # immunity_controller controller
    {
        'regexp': '',
        'app': 'immunity_controller.config',
        'include': {'module': '{app}.controller.urls', 'namespace': 'controller'},
    },
    # owm_legacy
    {
        'regexp': '',
        'app': 'owm_legacy',
        'include': {'module': '{app}.urls', 'namespace': 'owm'},
    },
    # immunity_controller.geo
    {
        'regexp': '',
        'app': 'immunity_controller.geo',
        'include': {'module': '{app}.api.urls', 'namespace': 'geo_api'},
    },
    # immunity_controller.config
    {
        'regexp': '',
        'app': 'immunity_controller.config',
        'include': {'module': '{app}.urls', 'namespace': 'config'},
    },
    # immunity_controller.config.api
    {
        'regexp': 'api/v1/',
        'app': 'immunity_controller.config',
        'include': {'module': '{app}.api.urls', 'namespace': 'config_api'},
    },
    # immunity_controller.connection
    {
        'regexp': '',
        'app': 'immunity_controller.connection',
        'include': {'module': '{app}.api.urls', 'namespace': 'connection_api'},
    },
]

urlpatterns = []

for meta in url_metadata:
    module = meta['include'].pop('module')
    if 'app' in meta:
        # if app attribute is specified, ensure the app is installed, or skip otherwise
        # this allows some flexibility during development or when trying custom setups
        if meta['app'] not in settings.INSTALLED_APPS:
            continue
        # DRY python module path
        module = module.format(**meta)
    urlpatterns.append(path(meta['regexp'], include(module, **meta['include'])))
