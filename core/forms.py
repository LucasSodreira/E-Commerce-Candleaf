from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'preco', 'categoria', 'imagem']
        widgets = {
            'nome': forms.TextInput(attrs={'id': 'titulo', 'placeholder': 'Informe o título do produto'}),
            'descricao': forms.Textarea(attrs={'id': 'descricao', 'cols': '30', 'rows': '6'}),
            'preco': forms.NumberInput(attrs={'id': 'valor', 'step': '0.01', 'placeholder': '0.00'}),
            'imagem': forms.FileInput(attrs={'id': 'imagem'}),
            'categoria': forms.Select(attrs={'id': 'categoria'}),
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'id': 'nome', 'placeholder': 'Informe o nome da categoria'}),
        }