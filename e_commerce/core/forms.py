# Importa ModelForm para criar formulários baseados em modelos
from django.forms import ModelForm
# Importa o formulário de criação de usuário padrão do Django
from django.contrib.auth.forms import UserCreationForm
# Importa a função que retorna o modelo de usuário ativo no projeto (core.User)
from django.contrib.auth import get_user_model
from django import forms
from .models import *

# Formulário para criar/editar produtos baseado no modelo Produto
class ProdutoForm(ModelForm):
    class Meta:
        model = Produto  # Modelo associado
        fields = ['nome', 'descricao', 'preco', 'categoria', 'imagem']  # Campos exibidos no formulário
        widgets = {
            'nome': forms.TextInput(attrs={'id': 'titulo', 'placeholder': 'Informe o título do produto'}),
            'descricao': forms.Textarea(attrs={'id': 'descricao', 'cols': '30', 'rows': '6'}),
            'preco': forms.NumberInput(attrs={'id': 'valor', 'step': '0.01', 'placeholder': '0.00'}),
            'imagem': forms.FileInput(attrs={'id': 'imagem'}),
            'categoria': forms.Select(attrs={'id': 'categoria'}),
        }

# Formulário de cadastro de usuário adaptado para usar o modelo User personalizado (core.User)
class UserCreateForm(UserCreationForm):
    class Meta:
        model = get_user_model()  # Usa core.User em vez de auth.User
        fields = ('username',)
