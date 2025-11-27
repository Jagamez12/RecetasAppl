from django.urls import path
from .views import CategoriaAPIView, CategoriaDetailAPIView
urlpatterns = [
    path('', CategoriaAPIView.as_view(), name='categoria-list'),
    path('<int:id>/', CategoriaDetailAPIView.as_view(), name='categoria-detail'),
]
