# Importações necessárias para as views
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, logout, login as auth_login
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.http import JsonResponse
from .forms import UserCreateForm
from django.contrib.auth.models import Group
from .decorators import group_required
from .models import *
from .forms import *

# View que lista todos os produtos (página inicial)
def listar_produtos(request):
    try:
        # Obtém o parâmetro de busca da URL, se existir
        nome_produto = request.GET.get('nome_produto', '')

        # Busca todas as categorias para o filtro
        categorias = Categoria.objects.all()

        # Filtra os produtos pelo nome informado (busca parcial, case-insensitive)
        produtos = Produto.objects.filter(nome__icontains=nome_produto)

        # Verifica se a requisição é AJAX (para busca sem recarregar a página)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            context = {'produtos': produtos}
            content = render_to_string('produtos_parcial.html', context)
            return HttpResponse(content)
        else:
            return render(request, 'index.html', {'produtos': produtos, 'categorias': categorias})

    except Exception as e:
        print(f"Erro na view listar_produtos: {e}")
        return JsonResponse({'html_produtos': ''})

# View que exibe a página de detalhes de um produto específico
def pag_product(request, id):
    produto = get_object_or_404(Produto, pk=id)
    return render(request, 'pag-product.html', {'produto': produto})

# View para editar um produto (restrita a administradores)
@group_required(['ADMINISTRADOR'])
def produto_editar(request, id):
    produto = get_object_or_404(Produto, id=id)

    if request.method == 'POST':
        # Se for POST, processa o formulário com os dados enviados
        form = ProdutoForm(request.POST, request.FILES, instance=produto)

        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        # Se for GET, exibe o formulário preenchido com os dados do produto
        form = ProdutoForm(instance=produto)

    return render(request, 'cadastro_pag.html', {'form': form})

# View para remover um produto (restrita a administradores)
@group_required(['ADMINISTRADOR'])
def produto_remover(request, id):
    produto = get_object_or_404(Produto, id=id)
    produto.delete()
    return redirect('index')

# View para criar um novo produto (restrita a administradores)
@group_required(['ADMINISTRADOR'])
def produto_criar(request):
    if request.method == 'POST':
        # Cria o formulário com os dados enviados e os arquivos (imagem)
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            # Salva o produto sem commitar para associar o usuário logado
            produto = form.save(commit=False)
            produto.user = request.user  # Define o usuário que cadastrou o produto
            produto.save()
            return redirect('index')
    else:
        form = ProdutoForm()

    return render(request, "cadastro_pag.html", {'form': form})

# View para realizar logout do usuário
def desconectar(request):
    logout(request)
    return redirect('index')

# View para realizar login do usuário
def login(request):
    # Se o usuário já estiver logado, redireciona para a página inicial
    if request.user.is_authenticated:
        return redirect('index')

    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Autentica o usuário com as credenciais fornecidas
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('index')

        else:
            return HttpResponse('Credenciais inválidas. Tente novamente.')

    return render(request, 'login.html')

# View para cadastro de novo usuário
def cadastro(request):
    # Se o usuário já estiver logado, redireciona para a página inicial
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = UserCreateForm()
        if request.method == 'POST':
            form = UserCreateForm(request.POST)

            if form.is_valid():
                user = form.save()

                # Associa o novo usuário ao grupo CLIENTE
                group = Group.objects.get(name='CLIENTE')
                user.groups.add(group)

                return redirect('login')

    return render(request, 'cadastro.html', {'form': form})
