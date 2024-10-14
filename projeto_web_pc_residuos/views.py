from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Olá, mundo. Esta é a página inicial do meu aplicativo.")

def home_view(request):
    return HttpResponse("Essa é a home page")

def exemplo_view(request):
    return HttpResponse("Essa é a view de exemplo")