from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Veiculo, Venda
from .serializers import *
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema



@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'veiculos-a-venda': reverse('veiculos_a_venda', request=request, format=format),
        'veiculos-vendidos': reverse('veiculos_vendidos', request=request, format=format),
        'comprar-veiculo': reverse('comprar_veiculo', request=request, format=format),
        'cadastrar-veiculo': reverse('cadastrar_veiculo', request=request, format=format),
    })

# 1. Cadastrar veículo
class VeiculoCreateView(generics.CreateAPIView):
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer

# 2. Editar veículo
class VeiculoUpdateView(generics.UpdateAPIView):
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer
    lookup_field = 'pk'

# 3. Listar veículos à venda
class VeiculosAVendaListView(generics.ListAPIView):
    queryset = Veiculo.objects.filter(vendido=False).order_by('preco')
    serializer_class = VeiculoSerializer

# 4. Listar veículos vendidos
class VeiculosVendidosListView(generics.ListAPIView):
    queryset = Veiculo.objects.filter(vendido=True).order_by('preco')
    serializer_class = VeiculoSerializer

# 5. Comprar veículo
class ComprarVeiculoView(APIView):
    @extend_schema(
        request=ComprarVeiculoRequestSerializer,
        responses=VendaSerializer,
        description="Realiza a compra de um veículo para um comprador previamente autenticado externamente."
        
    )
    @transaction.atomic
    def post(self, request):
        veiculo_id = request.data.get("veiculo_id")
        comprador_id_externo = request.auth.get('sub')
        valor = request.data.get("valor")

        veiculo = get_object_or_404(Veiculo, pk=veiculo_id)

        if veiculo.vendido:
            return Response({"erro": "Veículo já foi vendido."}, status=status.HTTP_400_BAD_REQUEST)

        venda = Venda.objects.create(
            veiculo=veiculo,
            comprador_id_externo=comprador_id_externo,
            valor=valor
        )

        veiculo.vendido = True
        veiculo.save()

        return Response(VendaSerializer(venda).data, status=status.HTTP_201_CREATED)


