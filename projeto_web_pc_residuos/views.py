from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from datetime import date
from datetime import datetime
import mysql.connector
from django.contrib.auth import logout
#import googlemaps

def conexao(user, password):
    try:
        return mysql.connector.connect(
            host='34.198.49.207',
            user=user,
            password=password,
            database='residuos_mineros'
        )
    except mysql.connector.Error as e:
        return HttpResponse(f"Erro na conexão com o banco de dados: {e}", status=500)

def index(request):
    return HttpResponse("Olá, mundo. Esta é a página inicial do meu aplicativo.")

def home_view(request):
    return render(request, 'template_home.html')

def exemplo_view(request):
    return HttpResponse("Essa é a view de exemplo")

def contato_view(request):
    return render(request, 'contato.html')  

def lista_residuos_view(request):
    conn = mysql.connector.connect(
        host='34.198.49.207',
        user='root',
        password='Admin12345',
        database='residuos_mineros'
    )

    cursor = conn.cursor(dictionary=True)  # Retorna resultados como dicionários, importante para enviar ao django

    query = """
    SELECT
        residuos.id_residuos,
        residuos.fecha_generacion
    FROM residuos;
    """
    
    cursor.execute(query)
    
    residuo = cursor.fetchall()  # Obter todos os resíduos

    cursor.close()
    conn.close()

    # Passar os dados do resíduo para o template
    return render(request, 'lista_residuos.html', {'residuo': residuo})

# Preciso adicionar um usuario
def adicionar_residuo_view(request):
    # Carrega todas as localizações para popular o formulário
    conn = mysql.connector.connect(
        host='34.198.49.207',
        user='root',
        password='Admin12345',
        database='residuos_mineros'
    )
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id_ubicaciones, nombre FROM ubicaciones")
    localizacoes = cursor.fetchall()
    cursor.close()
    conn.close()

    if request.method == "POST":
        # Captura de dados do formulário
        tipo_resido = request.POST.get("tipoResido") or None
        quantidade = request.POST.get("quantidade") or None
        unidad_medida = request.POST.get("unidad_medida") or None
        data_geracao = datetime.now() or None
        metodo_disposicao = request.POST.get("metodoDisposicao") or None
        estado = request.POST.get("estado") or None
        observacoes = request.POST.get("observacoes") or None
        id_localizacao = request.POST.get("localizacao") or None  # Captura o ID da localização selecionada
        id_usuario = 1  # usuário padrão

        conn = mysql.connector.connect(
            host='34.198.49.207',
            user='root',
            password='Admin12345',
            database='residuos_mineros'
        )
        cursor = conn.cursor()

        sql = """
            INSERT INTO residuos (tipo, cantidad, unidad_medida, fecha_generacion, notas, metodo_disposicion, estado, usuarios_id_usuario, ubicaciones_id_ubicaciones)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (tipo_resido, quantidade, unidad_medida, data_geracao, observacoes, metodo_disposicao, estado, id_usuario, id_localizacao)

        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('lista_de_residuos')

    # Caso não seja POST, renderize o formulário com as localizações
    return render(request, 'adicionar_residuo.html', {'localizacoes': localizacoes})



def perfil_residuo_view(request):
    conn = mysql.connector.connect(
        host='34.198.49.207',
        user='root',
        password='Admin12345',
        database='residuos_mineros'
    )

    cursor = conn.cursor(dictionary=True)  # Retorna resultados como dicionários, importante para enviar ao django

    
    residuo_id = request.GET.get('id_residuos')

    query = """
    SELECT
        residuos.id_residuos,
        residuos.tipo,
        residuos.cantidad,
        residuos.unidad_medida,
        residuos.fecha_generacion,
        residuos.notas,
        residuos.metodo_disposicion,
        residuos.estado,
        residuos.imagenes,
        usuarios.nombre AS usuario_nombre,
        usuarios.correo AS usuario_correo,
        ubicaciones.nombre AS ubicacion_nombre,
        ubicaciones.coordenadas AS ubicacion_coordenadas,
        ubicaciones.capacidad AS ubicacion_capacidad
    FROM residuos
    JOIN
        usuarios ON residuos.usuarios_id_usuario = usuarios.id_usuario
    JOIN
        ubicaciones ON residuos.ubicaciones_id_ubicaciones = ubicaciones.id_ubicaciones
    WHERE residuos.id_residuos = %s;
    """
    
    cursor.execute(query, (residuo_id,))
    
    residuo = cursor.fetchone()  # Obter o resíduo específico

    cursor.close()
    conn.close()

    # Passar os dados do resíduo para o template
    return render(request, 'perfil_residuo.html', {'residuo': residuo})


def deletar_residuo_view(request):
    if request.method == 'POST':
        id_residuo = request.POST.get('id_residuo')

        conn = mysql.connector.connect(
            host='34.198.49.207',
            user='root',
            password='Admin12345',
            database='residuos_mineros'
        )

        cursor = conn.cursor()
        cursor.execute("DELETE FROM residuos WHERE id_residuos = %s", (id_residuo,))
        conn.commit()
        cursor.close()
        conn.close()

    return redirect('lista_de_residuos')

# View para processar e atualizar os dados no banco
def editar_residuo_view(request):
    # Conexão com o banco de dados
    conn = mysql.connector.connect(
        host='34.198.49.207',
        user='root',
        password='Admin12345',
        database='residuos_mineros'
    )
    cursor = conn.cursor(dictionary=True)  # Retorna resultados como dicionários

    # Captura o ID do resíduo
    id_residuo = request.POST.get('id_residuo') or request.GET.get('id_residuo')

    if request.method == "POST":
        # Captura de dados do formulário
        tipo_resido = request.POST.get("tipoResido")
        quantidade = request.POST.get("quantidade")
        unidad_medida = request.POST.get("unidad_medida")
        metodo_disposicao = request.POST.get("metodoDisposicao")
        estado = request.POST.get("estado")
        observacoes = request.POST.get("observacoes")
        id_localizacao = request.POST.get("localizacao")  # Captura o ID da localização selecionada no formulário

        # Atualiza dados no banco
        try:
            sql = """
            UPDATE residuos 
            SET tipo = %s, cantidad = %s, unidad_medida = %s, metodo_disposicion = %s, estado = %s, notas = %s, ubicaciones_id_ubicaciones = %s
            WHERE id_residuos = %s
            """
            values = (tipo_resido, quantidade, unidad_medida, metodo_disposicao, estado, observacoes, id_localizacao, id_residuo)

            cursor.execute(sql, values)
            conn.commit()
            
            cursor.close()
            conn.close()
            return redirect('lista_de_residuos')  # Redirecionar após sucesso
        except Exception as e:
            print("Erro ao atualizar dados:", e)
    
    # Se for método GET, carrega os dados do resíduo para preencher o formulário
    sql_select = """
    SELECT 
        residuos.id_residuos, residuos.tipo, residuos.cantidad, residuos.unidad_medida, residuos.metodo_disposicion,
        residuos.estado, residuos.notas, residuos.ubicaciones_id_ubicaciones
    FROM residuos
    WHERE id_residuos = %s
    """
    cursor.execute(sql_select, (id_residuo,))
    residuo = cursor.fetchone()
    
    if not residuo:
        cursor.close()
        conn.close()
        return redirect('lista_de_residuos')  # Redireciona caso o resíduo não exista

    # Carrega todas as localizações do banco para popular no formulário
    cursor.execute("SELECT id_ubicaciones, nombre FROM ubicaciones")
    localizacoes = cursor.fetchall()

    cursor.close()
    conn.close()

    return render(request, 'editar_residuo.html', {'residuo': residuo, 'localizacoes': localizacoes})

    

import mysql.connector
import re  # Para usar expressões regulares para extrair coordenadas

import re
import mysql.connector
from django.shortcuts import render, redirect

def adicionar_localizacao_view(request):
    if request.method == 'POST':
        nome = request.POST.get('nome') or None
        coordenadas = request.POST.get('coordenadas', '') or None
        descricao = request.POST.get('descricao', '') or None
        tipo_localizacao = request.POST.get('tipo_localizacao', '') or None
        capacidade = request.POST.get('capacidade') or None
        
        # Extração das coordenadas (latitude e longitude)
        if coordenadas:
            # Usando expressão regular para capturar latitude e longitude
            match = re.match(r"Latitude: (-?\d+\.\d+), Longitude: (-?\d+\.\d+)", coordenadas)
            if match:
                latitude = float(match.group(1))
                longitude = float(match.group(2))
            else:
                # Se não encontrar o formato correto, defina latitude e longitude como None
                latitude, longitude = None, None
        else:
            latitude, longitude = None, None
        
        # Se latitude e longitude foram extraídos, armazene como string "latitude,longitude"
        if latitude is not None and longitude is not None:
            coordenadas = f"{latitude},{longitude}"
        else:
            coordenadas = None
        
        # Conectando-se ao banco de dados
        conn = mysql.connector.connect(
            host='34.198.49.207',
            user='root',
            password='Admin12345',
            database='residuos_mineros'
        )
        cursor = conn.cursor()

        # Agora, insira as coordenadas como string no banco de dados
        sql = """
            INSERT INTO ubicaciones (nombre, coordenadas, descripcion, tipo_ubicacion, capacidad)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (nome, coordenadas, descricao, tipo_localizacao, capacidade)
        cursor.execute(sql, values)
        
        conn.commit()
        cursor.close()
        conn.close()

        return redirect('lista_de_localizacoes')  # Redirecione após salvar
    
    return render(request, 'adicionar_localizacao.html')


def lista_localizacao_view(request):
    conn = conexao(user='root', password='Admin12345')
    cursor = conn.cursor()
    cursor.execute("SELECT id_ubicaciones, nombre, coordenadas, descripcion, tipo_ubicacion, capacidad FROM ubicaciones")
    localizacoes = cursor.fetchall()
    cursor.close()
    conn.close()
    return render(request, 'lista_localizacoes.html', {'localizacoes': localizacoes})

def deletar_localizacao_view(request):
    if request.method == 'POST':
        id_localizacao = request.POST.get('id')

        conn = conexao(user='root', password='Admin12345')
        cursor = conn.cursor()
        
        sql = "DELETE FROM ubicaciones WHERE id_ubicaciones = %s"
        cursor.execute(sql, (id_localizacao,))
        conn.commit()

        cursor.close()
        conn.close()

    return redirect('lista_de_localizacoes')  


def registrar_usuario_view(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        password = request.POST.get('password')
        rol = request.POST.get('rol')
        fecha_creacion = datetime.now()

        conn = conexao(user='root', password='Admin12345') # usuario padrão por enquanto
        cursor = conn.cursor()
        values = (nombre, correo, password, rol, fecha_creacion)
        sql = """
             INSERT INTO usuarios (nombre, correo, password, rol, fecha_creacion) 
             VALUES (%s, %s, %s, %s, %s)
             """
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()

        return redirect('/')
    else:
        return render(request, 'registrar_usuario.html')
    
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        password = request.POST.get('password')

        # Consulta no banco de dados externo
        conn = conexao(user='root', password='Admin12345')
        cursor = conn.cursor()
        sql = "SELECT * FROM usuarios WHERE correo = %s AND password = %s"
        values = (correo, password)
        cursor.execute(sql, values)
        usuario = cursor.fetchall()
        cursor.close()
        conn.close()

        if usuario:
            # Sincroniza com o sistema do Django
            try:
                user = User.objects.get(username=correo)
            except User.DoesNotExist:
                # Cria o usuário no sistema do Django, se não existir
                user = User.objects.create_user(username=correo, password=password)

            # Autentica e faz login
            user = authenticate(username=correo, password=password)
            if user:
                login(request, user)  # Cria a sessão do usuário
                return redirect('home')  # Redireciona para a página home inicial
        else:
            # Erro de login
            return render(request, 'login.html', {'error_message': 'El correo o la contraseña son incorrectos. / O email ou a senha estão incorretos'})
    else:
        # Exibe o formulário de login
        return render(request, 'login.html')

    
    
def perfil_localizacao_view(request):
    conn = mysql.connector.connect(
        host='34.198.49.207',
        user='root',
        password='Admin12345',
        database='residuos_mineros'
    )

    cursor = conn.cursor(dictionary=True)  # Retorna resultados como dicionários, importante para enviar ao django

    
    localizacao_id = request.GET.get('id')
    print("ID capturado:", localizacao_id)

    query = """
    SELECT
        ubicaciones.id_ubicaciones,
        ubicaciones.nombre,
        ubicaciones.coordenadas,
        ubicaciones.descripcion,
        ubicaciones.tipo_ubicacion,
        ubicaciones.capacidad
    FROM ubicaciones
    WHERE ubicaciones.id_ubicaciones = %s;
    """
    
    cursor.execute(query, (localizacao_id,))
    
    localizacao = cursor.fetchone()  # Obter o locazicao específico

    cursor.close()
    conn.close()

    # Passar os dados do localizacao para o template
    print(localizacao)
    return render(request, 'perfil_localizacao.html', {'localizacao': localizacao})
    
    
def editar_localizacao_view(request):
    # Conexão com o banco de dados
    conn = mysql.connector.connect(
        host='34.198.49.207',
        user='root',
        password='Admin12345',
        database='residuos_mineros'
    )
    cursor = conn.cursor(dictionary=True)

    # Capturando o ID da localização da requisição
    id_localizacao = request.POST.get('id_localizacao') or request.GET.get('id_localizacao')

    if request.method == "POST":
        # Capturando dados do formulário
        nome = request.POST.get('nome')
        coordenadas = request.POST.get('coordenadas')
        descricao = request.POST.get('descricao')
        tipo_localizacao = request.POST.get('tipo_localizacao')
        capacidade = request.POST.get('capacidade')

        try:
            # Atualizando os dados no banco
            sql = """
                UPDATE ubicaciones 
                SET nombre = %s, coordenadas = %s, descripcion = %s, tipo_ubicacion = %s, capacidad = %s
                WHERE id_ubicaciones = %s
            """
            values = (nome, coordenadas, descricao, tipo_localizacao, capacidade, id_localizacao)
            cursor.execute(sql, values)
            conn.commit()
            return redirect('lista_de_localizacoes')
        except Exception as e:
            print("Erro ao atualizar localização:", e)

    # Se for método GET ou falha no POST, carregamos os dados existentes
    sql_select = "SELECT * FROM ubicaciones WHERE id_ubicaciones = %s"
    cursor.execute(sql_select, (id_localizacao,))
    localizacao = cursor.fetchone()

    cursor.close()
    conn.close()

    if not localizacao:
        return redirect('lista_de_localizacoes')

    return render(request, 'editar_localizacao.html', {'localizacao': localizacao})



def logout_view(request):
    logout(request)
    return redirect('login')