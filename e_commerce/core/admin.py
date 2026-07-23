# Importa o admin do Django para registrar os modelos
from django.contrib import admin
# Importa UserAdmin para exibir o modelo User no admin com o layout padrão
from django.contrib.auth.admin import UserAdmin
from .models import Produto, Categoria, User

# Registra o modelo User personalizado no admin
admin.site.register(User, UserAdmin)

# Configuração da exibição do Produto no painel admin
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'preco', 'user')  # Colunas exibidas na listagem

admin.site.register(Produto, ProdutoAdmin)

# Configuração da exibição da Categoria no painel admin
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')

admin.site.register(Categoria, CategoriaAdmin)
