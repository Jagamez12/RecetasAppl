from django.urls import path
from .views import Class1, FotoEditarAPIView, FiltroRecetasPorSlug, HomeRecetasAPIView, RecetaBuscador



urlpatterns = [
    path('recetas-panel/<int:id>', Class1.as_view()),
    path('recetas-panel/editar/foto', FotoEditarAPIView.as_view()),
    path('recetas-panel/receta/slug/<str:slug>', FiltroRecetasPorSlug.as_view()),
    path('recetas-panel/recetas-home', HomeRecetasAPIView.as_view()),
    path('recetas-panel/recetas-buscador/', RecetaBuscador.as_view())
]
