from django.urls import path

from .views import schema

app_name = 'immunity_controller'
urlpatterns = [path('config/schema.json', schema, name='schema')]
