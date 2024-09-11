from ..utils import get_controller_urls
from . import views

app_name = 'immunity_controller'
urlpatterns = get_controller_urls(views)
