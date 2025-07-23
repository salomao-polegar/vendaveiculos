from django.urls import path
from .views import *

urlpatterns = [    
    path('', VeiculoCreateView.as_view(), name='cadastrar_veiculo'),
    path('<int:pk>/', VeiculoUpdateView.as_view(), name='editar_veiculo'),
    path('disponiveis/', VeiculosAVendaListView.as_view(), name='veiculos_a_venda'),
    path('vendidos/', VeiculosVendidosListView.as_view(), name='veiculos_vendidos'),
    path('comprar/', ComprarVeiculoView.as_view(), name='comprar_veiculo'),
]
