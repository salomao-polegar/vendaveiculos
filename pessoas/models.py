from django.db import models

# Create your models here.
class Pessoa(models.Model):
    id = models.CharField(max_length=100, primary_key=True) 
    nome=models.CharField(max_length=100)
    cpf_cnpj=models.CharField(max_length=11)
    data_nascimento=models.DateField()
    email=models.EmailField()