from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from datetime import date
from datetime import datetime
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

# Preciso adicionar um usuario
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

        id_ubicacion = 1  # Example, this should ideally come from another source

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

def adicionar_local_view(request):
    return render(request, 'adicionar_local.html')
