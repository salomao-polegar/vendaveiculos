from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from .serializers import *
from .models import *
from .auth0_utils import AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_CONNECTION, AUTH0_AUDIENCE
from rest_framework.permissions import IsAuthenticated
from .auth import IsAdminEmail

import requests
class CadastroClienteView(generics.CreateAPIView):
    serializer_class = CadastroClienteSerializer
    permission_classes = [IsAuthenticated, IsAdminEmail]
    
    def post(self, request):
        serializer = CadastroClienteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        payload = {
            "client_id": AUTH0_CLIENT_ID,
            "email": data["email"],
            "password": data["senha"],
            "connection": AUTH0_CONNECTION
        }
        url = f"https://{AUTH0_DOMAIN}/dbconnections/signup"
        res = requests.post(url, json=payload)
        
        if res.status_code == 400:
            res_json = res.json()
            if res_json.get("code") == "invalid_signup" and res_json.get("data", {}).get("identifierType") == "email":
                return Response({"erro": "E-mail já cadastrado"}, status=400)

        if res.status_code not in [200, 201]:
            return Response({"erro": "Erro ao criar usuário no Auth0", "detalhe": res.json()}, status=400)

        if res.status_code == 200:
            
            Pessoa.objects.create(
                nome=data["nome"],
                cpf_cnpj=data["cpf_cnpj"],
                data_nascimento=data["data_nascimento"],
                email=data["email"],
                id=res.json()["_id"]
        )
            
        return Response({"sucesso" : "Usuário " + res.json()["email"] + " criado com sucesso"}, status=201)
        
    
class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        payload = {
            "grant_type": "password",
            "username": data["email"],
            "password": data["senha"],
            "audience": AUTH0_AUDIENCE,
            "client_id": AUTH0_CLIENT_ID,
            "client_secret": AUTH0_CLIENT_SECRET,
            "scope": "openid profile email",
            "realm": AUTH0_CONNECTION
        }
        url = f"https://{AUTH0_DOMAIN}/oauth/token"
        res = requests.post(url, json=payload)
        if res.status_code == 200:
            return Response(res.json(), status=200)
        return Response(res.json(), status=res.status_code)

