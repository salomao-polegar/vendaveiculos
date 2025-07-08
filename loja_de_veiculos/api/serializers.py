from rest_framework import serializers
from .models import *

class VeiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veiculo
        fields = '__all__'

class VendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venda
        fields = '__all__'


class ComprarVeiculoRequestSerializer(serializers.Serializer):
    veiculo_id = serializers.IntegerField(help_text="ID do veículo a ser comprado")
    comprador_id_externo = serializers.CharField(help_text="ID externo do comprador autenticado")
    valor = serializers.DecimalField(max_digits=10, decimal_places=2, help_text="Valor da compra")
