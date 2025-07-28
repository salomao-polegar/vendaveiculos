from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404
from django.db import transaction
from drf_spectacular.utils import extend_schema
from pessoas.auth import get_userinfo, IsAdminEmail

# 1. Cadastrar veículo
class VeiculoCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminEmail]
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer

    def create(self, request, *args, **kwargs):
        is_many = isinstance(request.data, list)

        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

# 2. Editar veículo
class VeiculoUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdminEmail]
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer
    lookup_field = 'pk'
    
class VeiculoDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminEmail]
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer
    lookup_field = 'pk'

# 3. Listar veículos à venda
class VeiculosAVendaListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Veiculo.objects.filter(vendido=False).order_by('preco')
    serializer_class = VeiculoSerializer

# 4. Listar veículos vendidos
class VeiculosVendidosListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Veiculo.objects.filter(vendido=True).order_by('preco')
    serializer_class = VeiculoSerializer

# 5. Comprar veículo
class ComprarVeiculoView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        request=ComprarVeiculoRequestSerializer,
        responses=VendaSerializer,
        description="Realiza a compra de um veículo para um comprador previamente autenticado externamente."
        
    )
    @transaction.atomic
    def post(self, request):
        veiculo_id = request.data.get("veiculo_id")
        
        veiculo = get_object_or_404(Veiculo, pk=veiculo_id)

        if veiculo.vendido:
            return Response({"erro": "Veículo já foi vendido."}, status=status.HTTP_400_BAD_REQUEST)

        comprador = Pessoa.objects.get(email=get_userinfo(request)['email'])

        venda = Venda.objects.create(
            veiculo=veiculo,
            comprador=comprador,
            data_compra=datetime.now(),
            valor=veiculo.preco
        )

        veiculo.vendido = True
        venda.save()
        veiculo.save()        

        return Response(VendaSerializer(venda).data, status=status.HTTP_201_CREATED)


class HelloView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return Response({"error": "Token não enviado"}, status=401)

        token = auth_header.split(' ')[1]
        userinfo = get_userinfo(token)

        if not userinfo:
            return Response({"error": "Não foi possível obter dados do usuário"}, status=400)

        return Response({
            "msg": "Autenticado com sucesso",
            "usuario": {
                "email": userinfo.get("email"),
            }
        })