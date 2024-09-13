from ..utils import get_geo_urls
from . import views as geo_views

app_name = 'immunity_controller'

urlpatterns = get_geo_urls(geo_views)
