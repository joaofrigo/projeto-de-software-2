from django.shortcuts import redirect
from django.contrib.auth import logout
from django.urls import reverse

class LoginRequiredMiddleware:
    """
    Middleware que força autenticação para todas as views, exceto a página de login.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Adicione um print para verificar a URL que está sendo acessada
        print(f"Acessando URL: {request.path}")

        # Verifica se a URL atual é a página de login pelo nome da URL
        if not request.user.is_authenticated and request.path != reverse('login'):
            print("Usuário não autenticado. Redirecionando para o login.")
            return redirect('login')
        
        return self.get_response(request)





