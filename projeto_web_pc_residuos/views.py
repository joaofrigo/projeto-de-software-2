from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Olá, mundo. Esta é a página inicial do meu aplicativo.")

def home_view(request):
    return render(request, 'template_home.html')

def exemplo_view(request):
    return HttpResponse("Essa é a view de exemplo")

def contato_view(request):
    return render(request, 'contato.html')  

def lista_residuos_view(request):
    return render(request, 'lista_residuos.html')  

def adicionar_residuo_view(request):
    return render(request, 'adicionar_residuo.html') 