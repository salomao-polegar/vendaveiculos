from rest_framework import serializers
from .models import *

class VeiculoListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        return [self.child.create(attrs) for attrs in validated_data]

class VeiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veiculo
        fields = '__all__'
        list_serializer_class = VeiculoListSerializer

class VendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venda
        fields = '__all__'

class ComprarVeiculoRequestSerializer(serializers.Serializer):
    veiculo_id = serializers.IntegerField(help_text="ID do veículo a ser comprado")
    
