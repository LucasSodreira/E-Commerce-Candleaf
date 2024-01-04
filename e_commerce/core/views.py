from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

def pag_product(request):
    return render(request, 'pag-product.html')

def panel(request):
    return render(request, 'panel.html')