from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, logout, login as auth_login
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .decorators import group_required
from .models import *
from .forms import *

# Create your views here.

def listar_produtos(request):
    try:
        nome_produto = request.GET.get('nome_produto', '')
        categoria_id = request.GET.get('categoria', None)  # Corrigido para 'categoria'
        
        categorias = Categoria.objects.all()
        
        # Filtra os produtos pelo nome, se fornecido
        produtos = Produto.objects.all()
        if nome_produto:
            produtos = produtos.filter(nome__icontains=nome_produto)
        
        # Filtra os produtos pela categoria, se fornecido
        if categoria_id:
            produtos = produtos.filter(categoria_id=categoria_id)
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            context = {'produtos': produtos}
            content = render_to_string('produtos_parcial.html', context)
            return HttpResponse(content)
        else:
            return render(request, 'index.html', {'produtos': produtos, 'categorias': categorias})
    
    except Exception as e:
        print(f"Erro na view listar_produtos: {e}")
        return JsonResponse({'html_produtos': ''})


def pag_product(request, id):
    produto = get_object_or_404(Produto, pk=id)
    return render(request, 'pag-product.html', {'produto': produto})


# Se o método HTTP for POST e o formulário for válido, o produto é atualizado. 
# Se for GET, o formulário é preenchido com os detalhes do produto existente.
@group_required(['ADMINISTRADOR'])
def produto_editar(request, id):
    produto = get_object_or_404(Produto, id=id)
   
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance = produto)

        if form.is_valid():
            form.instance.created_by = request.user
            form.save()
            return redirect('index')
    else:
        form = ProdutoForm(instance=produto)

    return render(request,'cadastro_pag.html', {'form': form})

# Se um produto com o ID fornecido existir, ele é excluído e a página é redirecionada para 'index'.
@group_required(['ADMINISTRADOR'])
def produto_remover(request, id):
    produto = get_object_or_404(Produto, id=id)
    produto.delete()
    return redirect('index')


@group_required(['ADMINISTRADOR'])
def produto_criar(request):

    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            produto = form.save(commit=False)
            produto.criado_por = request.user
            form.save()
            return redirect('index')  # Redireciona para uma página de sucesso
    else:
        form = ProdutoForm()

    return render(request, "cadastro_pag.html", {'form': form})


def categoria_product(request, id):
    categoria = get_object_or_404(Categoria, pk=id)
    return render(request, 'pag_categoria.html', {'produto': categoria})


@group_required(['ADMINISTRADOR'])
def categoria_remover(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    categoria.delete()
    return redirect('index')

@group_required(['ADMINISTRADOR'])
def categoria_criar(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.instance.created_by = request.user
            form.save()
            return redirect('index')  # Redireciona para uma página de sucesso
    else:
        form = CategoriaForm()

    return render(request, "categoria.html", {'form': form})

@group_required(['ADMINISTRADOR'])
def categoria_editar(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    nome_produto = request.GET.get('nome_produto', '')
        
    categorias = Categoria.objects.all()
    # Faça a filtragem com base nos parâmetros recebidos
    produtos = Produto.objects.filter(nome__icontains=nome_produto)
   
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance = categoria)

        if form.is_valid():
            form.instance.created_by = request.user
            form.save()
            return redirect('index')
    else:
        form = CategoriaForm(instance=categoria)

    return render(request,'edit_categoria.html', {'form': form, 'produtos': produtos, 'categorias': categorias})




def desconectar(request):
    logout(request)
    return redirect('index')


def login(request):
    # Se o usuário já estiver logado, redireciona para a página inicial
    if request.user.is_authenticated:
        return redirect('index')
    
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None: # Se o usuário existir, faz o login
            auth_login(request, user)
            return redirect('index')
        
        else:
            return HttpResponse('Credenciais inválidas. Tente novamente.')

    return render(request, 'login.html')

def cadastro(request):
    # Se o usuário já estiver logado, redireciona para a página inicial
    if request.user.is_authenticated:
        return redirect('index')
    
    else:
        # Cria um formulário de cadastro
        form = UserCreationForm()
        
        # Se o formulário for válido, salva o usuário no banco de dados
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            
            if form.is_valid():
                user = form.save(commit=False)
                user.save()
            
                group = Group.objects.get(name='CLIENTE')
                user.groups.add(group)
                
                return redirect('login')
            else:
                return HttpResponse(f'Erro ao cadastrar usuário. Tente novamente. {form.errors}')   

    return render(request, 'cadastro.html', {'form': form})