from django.db import models
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nome
    
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='produtos/', null=True, blank=True, max_length=255)
    
    def __str__(self):
        return self.nome

class User(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='core_users')
    user_permissions = models.ManyToManyField(Permission, related_name='core_user_permissions')