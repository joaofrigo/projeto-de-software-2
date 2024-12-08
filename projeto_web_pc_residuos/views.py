from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime
import mysql.connector
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
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

@login_required
def index(request):
    return HttpResponse("Olá, mundo. Esta é a página inicial do meu aplicativo.")

@login_required
def home_view(request):
    return render(request, 'template_home.html')

@login_required
def exemplo_view(request):
    return HttpResponse("Essa é a view de exemplo")

@login_required
def contato_view(request):
    return render(request, 'contato.html')  

@login_required
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

@login_required
def adicionar_residuo_view(request):
    if request.method == "POST":
        tipo_resido = request.POST.get("tipoResido") or None
        quantidade = request.POST.get("quantidade") or None
        unidad_medida = request.POST.get("unidad_medida") or None
        data_geracao = datetime.now() or None
        metodo_disposicao = request.POST.get("metodoDisposicao") or None
        estado = request.POST.get("estado") or None
        imagens = request.FILES.getlist("imagens")
        observacoes = request.POST.get("observacoes") or None
        id_usuario = 1  # usuario padrão

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

        id_ubicacion = 1 
        id_ubicacion = 1 

        imagem_nome = None
        if imagens:
            imagem_nome = imagens[0].name
    

        values = (tipo_resido, quantidade, unidad_medida, data_geracao, observacoes, metodo_disposicao, estado, id_usuario, id_ubicacion)
        cursor.execute(sql, values)

        conn.commit()

        cursor.close()
        conn.close()
        return redirect('lista_de_residuos')

    return render(request, 'adicionar_residuo.html')


@login_required
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

@login_required
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

@login_required
def editar_residuo_view(request):
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
        residuos.metodo_disposicion,
        residuos.estado,
        residuos.imagenes,
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
    return render(request, 'editar_residuo.html', {'residuo': residuo})

@login_required
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

@login_required
def lista_localizacao_view(request):
    conn = conexao(user='root', password='Admin12345')
    cursor = conn.cursor()
    cursor.execute("SELECT id_ubicaciones, nombre, coordenadas, descripcion, tipo_ubicacion, capacidad FROM ubicaciones")
    localizacoes = cursor.fetchall()
    cursor.close()
    conn.close()
    return render(request, 'lista_localizacoes.html', {'localizacoes': localizacoes})

@login_required
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

@login_required
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

   
def login_view(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        password = request.POST.get('password')

        # Conexão ao banco de dados usando sua função
        conn = conexao(user='root', password='Admin12345')
        cursor = conn.cursor()

        try:
            # Verifica se o usuário existe no banco de dados legado
            sql = """
                SELECT correo FROM usuarios WHERE correo = %s AND password = %s
            """
            values = (correo, password)
            cursor.execute(sql, values)
            usuario = cursor.fetchall()  # Retorna apenas uma linha
        finally:
            cursor.close()
            conn.close()

        if usuario:  # Usuário encontrado
            correo_db = usuario[0]

            # Verifica se o usuário já existe no modelo Django User
            user, created = User.objects.get_or_create(username=correo_db)

            # Faz login do usuário no Django
            login(request, user)
            return redirect('home')  # Redireciona para a página inicial protegida
        else:
            # Retorna mensagem de erro caso usuário não exista no banco legado
            return render(request, 'login.html', {'error_message': 'El correo o la contraseña son incorrectos. / O email ou a senha estão incorretos'})
    else:
        return render(request, 'login.html')

