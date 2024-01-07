from django.contrib import admin
from .models import Produto, Categoria

# Register your models here.

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'preco')

admin.site.register(Produto, ProdutoAdmin)

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    
admin.site.register(Categoria, CategoriaAdmin)
