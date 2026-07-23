# Importa as ferramentas do Django para criar modelos de banco de dados
from django.db import models
# Importa os modelos Group e Permission para controle de permissões
from django.contrib.auth.models import Group, Permission
# Importa a classe abstrata base para criar um modelo de usuário personalizado
from django.contrib.auth.models import AbstractUser
# Importa as configurações do projeto (ex: AUTH_USER_MODEL)
from django.conf import settings

# Modelo de usuário personalizado que substitui o User padrão do Django
class User(AbstractUser):
    # Define um related_name diferente para evitar conflito com o auth.User original
    groups = models.ManyToManyField(Group, related_name='core_users')
    user_permissions = models.ManyToManyField(Permission, related_name='core_user_permissions')

# Modelo que representa uma categoria de produto
class Categoria(models.Model):
    nome = models.CharField(max_length=100)  # Nome da categoria (ex: Velas, Aromatizantes)

    def __str__(self):
        return self.nome

# Modelo que representa um produto do e-commerce
class Produto(models.Model):
    nome = models.CharField(max_length=100)  # Nome do produto
    descricao = models.TextField()  # Descrição detalhada do produto
    preco = models.DecimalField(max_digits=8, decimal_places=2)  # Preço com 2 casas decimais
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)  # Categoria do produto
    imagem = models.ImageField(upload_to='produtos/', null=True, blank=True, max_length=255)  # Imagem do produto
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Usuário que cadastrou o produto

    def __str__(self):
        return self.nome
