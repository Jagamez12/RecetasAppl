from django.urls import path
from .views import RecetasAPIView, RecetaDetailAPIView

urlpatterns = [
    path('', RecetasAPIView.as_view(), name='recetas_list'),
    path('<int:id>/', RecetaDetailAPIView.as_view(), name='receta_detail'),
]
