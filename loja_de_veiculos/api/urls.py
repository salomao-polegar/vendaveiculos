# api/urls.py

from django.urls import path
from .views import (
    VeiculoCreateView,
    VeiculoUpdateView,
    VeiculosAVendaListView,
    VeiculosVendidosListView,
    ComprarVeiculoView,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)



urlpatterns = [
    path('veiculos/', VeiculoCreateView.as_view(), name='cadastrar_veiculo'),
    path('veiculos/<int:pk>/', VeiculoUpdateView.as_view(), name='editar_veiculo'),
    path('veiculos-a-venda/', VeiculosAVendaListView.as_view(), name='veiculos_a_venda'),
    path('veiculos-vendidos/', VeiculosVendidosListView.as_view(), name='veiculos_vendidos'),
    path('comprar-veiculo/', ComprarVeiculoView.as_view(), name='comprar_veiculo'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
