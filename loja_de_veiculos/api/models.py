from django.db import models

# Create your models here.

class Veiculo(models.Model):
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    ano = models.IntegerField()
    cor = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    vendido = models.BooleanField(default=False)

class Venda(models.Model):
    veiculo = models.OneToOneField(Veiculo, on_delete=models.CASCADE)
    comprador_id_externo = models.CharField(max_length=255)  # ID vindo do serviço de auth externo
    data = models.DateTimeField(auto_now_add=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)