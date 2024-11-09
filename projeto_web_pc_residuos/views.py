from django.shortcuts import render
from django.http import HttpResponse
from datetime import date
import mysql.connector


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

def adicionar_residuo_view(request):
    conn = mysql.connector.connect(
        host='34.198.49.207',
        user='root',
        password='Admin12345',
        database='residuos_mineros'
    )
    return render(request, 'adicionar_residuo.html')

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
