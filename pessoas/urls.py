from django.urls import path
from pessoas.views import *

urlpatterns = [
    path('cadastro/', CadastroClienteView.as_view()),
    path('login/', LoginView.as_view()),   
]