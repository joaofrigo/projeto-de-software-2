from django.contrib import admin
from django.urls import include, path
from .views import *


urlpatterns = [
    path('', home_view, name='home'),  
    path('exemplo/', exemplo_view, name='exemplo'),  
    path('contato/', contato_view, name='contate_a_gente'),  
    path('lista_residuos/', lista_residuos_view, name='lista_de_residuos'),
    path('adicionar_residuo/', adicionar_residuo_view, name='adicionar_residuo'), 
    path('perfil_residuo/', perfil_residuo_view, name='perfil_residuo'),
    path('deletar_residuo/', deletar_residuo_view, name='deletar_residuo'),
    path('adicionar_localizacao/', adicionar_localizacao_view, name='adicionar_localizacao'),
    path('lista_localizacao/', lista_localizacao_view, name='lista_de_localizacoes'),
    #path('erro_conexao_mysql', erro_conexao_mysql_view, name='erro_conexao_mysql')
]
