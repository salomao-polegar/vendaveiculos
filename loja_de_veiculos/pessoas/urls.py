from django.contrib import admin
from django.urls import path
from pessoas.views import *

urlpatterns = [
    path('cadastrar-cliente/', CadastroClienteView.as_view(), name='cadastrar_cliente'),
]