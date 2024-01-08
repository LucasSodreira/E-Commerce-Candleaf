from django.shortcuts import render
from django.shortcuts import render,get_object_or_404,redirect
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.http import JsonResponse
from .models import *
from .forms import *

# Create your views here.

def listar_produtos(request):
    try:
        nome_produto = request.GET.get('nome_produto', '')
        # filtro = request.GET.get('filtro', '')
        
        categorias = Categoria.objects.all()
        
        # Faça a filtragem com base nos parâmetros recebidos
        produtos = Produto.objects.filter(nome__icontains=nome_produto)

        # if filtro:
        #     produtos = produtos.filter(seu_campo_de_filtro=filtro)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            context = {'produtos': produtos}
            content = render_to_string('produtos_parcial.html', context)
            return HttpResponse(content)  # Usando HttpResponse para retornar a string diretamente
        else:
            return render(request, 'index.html', {'produtos': produtos, 'categorias': categorias})
        
    except Exception as e:
        # Imprima o erro no console
        print(f"Erro na view listar_produtos: {e}")
        return JsonResponse({'html_produtos': ''})



def pag_product(request, id):
    produto = get_object_or_404(Produto, pk=id)
    
    return render(request, 'pag-product.html', {'produto': produto})


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


def produto_remover(request, id):
    produto = get_object_or_404(Produto, id=id)
    produto.delete()
    return redirect('index')


def produto_criar(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redireciona para uma página de sucesso
    else:
        form = ProdutoForm()

    return render(request, "cadastro_pag.html", {'form': form})

def login(request):
    return render(request, 'login.html')

def cadastro(request):
    return render(request, 'cadastro.html')