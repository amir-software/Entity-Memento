from .memento_views import *

from django.urls import path


urlpatterns = [
    path("memento/product_memento/", ProductManagement.as_view())
]