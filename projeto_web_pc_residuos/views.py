from django.shortcuts import render
from django.http import HttpResponse
from datetime import date


def index(request):
    return HttpResponse("Olá, mundo. Esta é a página inicial do meu aplicativo.")

def home_view(request):
    return render(request, 'template_home.html')

def exemplo_view(request):
    return HttpResponse("Essa é a view de exemplo")

def contato_view(request):
    return render(request, 'contato.html')  

def lista_residuos_view(request):
    # Dados mockados
    residuos = [
        {'nome': 'Resíduo A', 'data_geracao': date(2023, 10, 1)},
        {'nome': 'Resíduo B', 'data_geracao': date(2023, 10, 5)},
        {'nome': 'Resíduo C', 'data_geracao': date(2023, 10, 10)},
        {'nome': 'Resíduo D', 'data_geracao': date(2023, 10, 12)},
        {'nome': 'Resíduo E', 'data_geracao': date(2023, 10, 15)},
        {'nome': 'Resíduo F', 'data_geracao': date(2023, 10, 18)},
        {'nome': 'Resíduo G', 'data_geracao': date(2023, 10, 20)},
        {'nome': 'Resíduo H', 'data_geracao': date(2023, 10, 22)},
    ]
    return render(request, 'lista_residuos.html', {'residuos': residuos}) 

def adicionar_residuo_view(request):
    return render(request, 'adicionar_residuo.html') 

def perfil_residuo_view(request):
    return render(request, 'perfil_residuo.html') 