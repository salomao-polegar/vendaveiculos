from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CadastroClienteSerializer
from .models import Pessoa
from .auth0_utils import get_auth0_management_token, AUTH0_DOMAIN, AUTH0_CONNECTION
import requests
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny



class CadastroClienteView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        request=CadastroClienteSerializer,
        responses={201: None, 400: dict},
        description="Cadastra um novo cliente no Auth0 e no banco local."
    )
    def post(self, request):
        serializer = CadastroClienteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # 1. Criar no Auth0
        try:
            token = get_auth0_management_token()
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            payload = {
                "email": data["email"],
                "password": data["senha"],
                "connection": AUTH0_CONNECTION,
                "name": data["nome"]
            }
            res = requests.post(f"https://{AUTH0_DOMAIN}/api/v2/users", headers=headers, json=payload)
            res.raise_for_status()
            auth0_user = res.json()
        except requests.exceptions.RequestException as e:
            return Response({
                "erro": "Erro ao criar usuário no Auth0",
                "detalhe": str(e),
                "resposta_auth0": res.json() if res else None  # 👈 mostra o erro da resposta
            }, status=400)
            

        # 2. Criar localmente no banco do Django
        Pessoa.objects.create( 
            nome=data["nome"],
            cpf_cnpj=data["cpf_cnpj"],
            data_nascimento=data["data_nascimento"]
        )

        return Response({"mensagem": "Cliente cadastrado com sucesso."}, status=status.HTTP_201_CREATED)
