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
        
        categorias = Categoria.objects.all()
        
        # Faça a filtragem com base nos parâmetros recebidos
        produtos = Produto.objects.filter(nome__icontains=nome_produto)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            context = {'produtos': produtos}
            content = render_to_string('produtos_parcial.html', context)
            return HttpResponse(content)  # Usando HttpResponse para retornar a string diretamente
        else:
            return render(request, 'index.html', {'produtos': produtos, 'categorias': categorias})
        
    except Exception as e:
        print(f"Erro na view listar_produtos: {e}")
        return JsonResponse({'html_produtos': ''})


def pag_product(request, id):
    produto = get_object_or_404(Produto, pk=id)
    return render(request, 'pag-product.html', {'produto': produto})


@group_required(['ADMINISTRADOR'])
def produto_editar(request,id):
    produto = get_object_or_404(Produto, id=id)
   
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance = produto)

        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ProdutoForm(instance=produto)

    return render(request,'cadastro_pag.html', {'form': form})

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
            form.save()
            return redirect('index')  # Redireciona para uma página de sucesso
    else:
        form = ProdutoForm()

    return render(request, "cadastro_pag.html", {'form': form})

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

        if user is not None:
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

    return render(request, 'cadastro.html', {'form': form})