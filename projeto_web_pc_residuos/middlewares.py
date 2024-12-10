from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import logout

class LoginRequiredMiddleware:
    """
    Middleware que força autenticação para todas as páginas,
    redirecionando usuários não autenticados para a página de login.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(f"Acessando URL: {request.path}")

        # URL de login
        login_url = reverse('login')

        # Exceções: Página de login e favicon
        if request.path in ['/', '/favicon.ico'] or request.path == login_url:
            print('Exceção de URL: Permitir acesso sem redirecionar')
            return self.get_response(request)
        
        '''
        # Caso o usuário acesse a página de contato, deslogar
        if request.path == reverse('contate_a_gente'):
            print("Usuário acessou a página de contato. Fazendo logout.")
            logout(request)
            return redirect(login_url)
        '''
        
        # Verifica se o usuário está autenticado
        if not request.user.is_authenticated:
            print("Usuário não autenticado. Redirecionando para o login.")
            return redirect(login_url)

        
        elif request.user.is_authenticated:
            # Usuário autenticado: continuar normalmente
            print("Usuário autenticado. Permitir acesso.")
            return self.get_response(request)
