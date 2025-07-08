from rest_framework import serializers


class CadastroClienteSerializer(serializers.Serializer):
    nome = serializers.CharField()
    email = serializers.EmailField()
    senha = serializers.CharField(write_only=True)
    cpf_cnpj = serializers.CharField()
    data_nascimento = serializers.DateField()