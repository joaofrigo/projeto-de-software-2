import mysql.connector

print("Conectando")
conn = mysql.connector.connect(
    host='34.198.49.207',
    user='root',
    password='Admin12345',
    database='residuos_mineros'
)
print("Conectado")

cursor = conn.cursor()

query = 'SELECT * FROM usuarios;'
cursor.execute(query)
resultados = cursor.fetchall()

for linha in resultados:
    print(linha)

query = 'DESCRIBE usuarios;'
cursor.execute(query)
resultados = cursor.fetchall()

for linha in resultados:
    print(linha)

print("\n")
query = 'SELECT * FROM residuos;'
cursor.execute(query)
resultados = cursor.fetchall()

for linha in resultados:
    print(linha)

print("\n")
query = 'DESCRIBE residuos;'
cursor.execute(query)
resultados = cursor.fetchall()

for linha in resultados:
    print(linha)

print("\n")
query = 'DESCRIBE ubicaciones'
cursor.execute(query)
resultados = cursor.fetchall()

for linha in resultados:
    print(linha)


cursor.close()
conn.close()
print("Conexão encerrada.")


'''
tables totais:
('disposiciones',)
('eventos_log',)
('reportes',)
('residuos',)
('ubicaciones',)
('usuarios',)
'''



"""
-- Tabla de usuarios
CREATE TABLE usuarios (
    id_usuario SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL UNIQUE,
    contraseña VARCHAR(100) NOT NULL,
    rol VARCHAR(50) CHECK(rol IN ('operador', 'supervisor', 'administrador')) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de residuos
CREATE TABLE residuos (
    id_residuo SERIAL PRIMARY KEY,
    tipo VARCHAR(50) CHECK(tipo IN ('peligroso', 'no peligroso', 'reciclable')) NOT NULL,
    cantidad DECIMAL(10, 2) NOT NULL,
    unidad_medida VARCHAR(10) CHECK(unidad_medida IN ('kg', 'litros')) NOT NULL,  -- Agregado: unidad de medida
    fecha_generacion DATE NOT NULL,
    id_ubicacion INTEGER,
    imagen VARCHAR(255),
    notas TEXT,
    FOREIGN KEY(id_ubicacion) REFERENCES ubicaciones(id_ubicacion)
);

-- Tabla de características dinámicas
CREATE TABLE caracteristicas (
    id_caracteristica SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo_valor VARCHAR(50) CHECK(tipo_valor IN ('booleano', 'entero', 'decimal', 'texto')) NOT NULL
);

-- Tabla asociativa para características de residuos
CREATE TABLE residuos_caracteristicas (
    id_residuo INTEGER,
    id_caracteristica INTEGER,
    valor TEXT NOT NULL,
    PRIMARY KEY(id_residuo, id_caracteristica),
    FOREIGN KEY(id_residuo) REFERENCES residuos(id_residuo),
    FOREIGN KEY(id_caracteristica) REFERENCES caracteristicas(id_caracteristica)
);

-- Tabla de disposiciones
CREATE TABLE disposiciones (
    id_disposicion SERIAL PRIMARY KEY,
    id_residuo INTEGER,
    metodo_disposicion VARCHAR(50) CHECK(metodo_disposicion IN ('reciclaje', 'almacenamiento', 'eliminación')) NOT NULL,
    estado_disposicion VARCHAR(50) CHECK(estado_disposicion IN ('pendiente', 'en proceso', 'completado')) NOT NULL,
    fecha_disposicion DATE,
    notas TEXT,
    FOREIGN KEY(id_residuo) REFERENCES residuos(id_residuo)
);

-- Tabla de ubicaciones
CREATE TABLE ubicaciones (
    id_ubicacion SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    coordenadas VARCHAR(50),
    capacidad DECIMAL(10, 2) NOT NULL,  -- Agregado: capacidad máxima de la ubicación
    descripcion TEXT
);

-- Tabla de reportes
CREATE TABLE reportes (
    id_reporte SERIAL PRIMARY KEY,
    id_usuario INTEGER,
    fecha_reporte TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    contenido TEXT,
    FOREIGN KEY(id_usuario) REFERENCES usuarios(id_usuario)
);

-- Tabla de eventos de auditoría (agregado para auditoría)
CREATE TABLE eventos_log (
    id_evento SERIAL PRIMARY KEY,
    id_usuario INTEGER,
    accion VARCHAR(50) NOT NULL,  -- Acción realizada (ej: 'crear_residuo', 'modificar_disposicion')
    id_referencia INTEGER,        -- Referencia al id del objeto afectado
    tabla_referencia VARCHAR(50), -- Tabla afectada (ej: 'residuos', 'disposiciones')
    fecha_evento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    detalles TEXT,
    FOREIGN KEY(id_usuario) REFERENCES usuarios(id_usuario)
);






                        <!-- <form method="post" action="{% url 'deletar_localizacao' %}">
                            {% csrf_token %}
                            <input type="hidden" name="id" value="{{ localizacao.id }}">
                            <button type="submit" class="btn-deletar">Deletar</button>
                        </form> -->
                        form do botão de delete de lista_localização
"""

