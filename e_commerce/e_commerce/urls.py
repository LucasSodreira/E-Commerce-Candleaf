# Configuração de rotas (URLs) do projeto e_commerce

from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from core.views import *
from django.conf import settings

# Lista de padrões de URL do projeto
urlpatterns = [
    path('admin/', admin.site.urls),  # Rota para o painel administrativo

    path('', listar_produtos, name='index'),  # Página inicial com listagem de produtos
    path('cadastro_produto/', produto_criar, name='cadastro_produto'),  # Cadastro de novo produto

    path('produto/<int:id>/', pag_product, name='pag_product'),  # Página de detalhe do produto
    path('produto/editar/<int:id>/', produto_editar, name='produto_editar'),  # Edição de produto
    path('produto/remover/<int:id>/',produto_remover, name='produto_remover'),  # Remoção de produto

    path('login/', login, name='login'),  # Página de login
    path('cadastro/', cadastro, name='cadastro'),  # Página de cadastro de usuário
    path('desconectar/', desconectar, name='desconectar'),  # Logout do usuário

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)  # Servir arquivos de mídia em desenvolvimento
