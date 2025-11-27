from django.urls import path
from .views import *

urlpatterns = [
    path('', ContactoAPIView.as_view(), name='contacto_api'),
]
