from django.db import models
from pessoas.models import Pessoa

# Create your models here.

class Veiculo(models.Model):
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    ano = models.IntegerField()
    cor = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    vendido = models.BooleanField(default=False)

class Venda(models.Model):
    veiculo = models.ForeignKey(to=Veiculo, on_delete=models.CASCADE)
    comprador = models.ForeignKey(to=Pessoa, on_delete=models.CASCADE)
    data_compra = models.DateTimeField(auto_now_add=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)