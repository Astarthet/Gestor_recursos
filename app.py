z|import sqlite3
import pandas as pd
from flask import Flask, request, render_template, redirect, url_for

# Configuración del servidor Flask
app = Flask(__name__)

# Inicializar la base de datos
def init_db():
    conn = sqlite3.connect('gestion_recursos.db')
    cursor = conn.cursor()
    # Crear tabla para empleados
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS empleados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            puesto TEXT NOT NULL,
            horas_trabajadas INTEGER,
            eficiencia REAL
        )
    ''')
    # Crear tabla para infraestructura
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS infraestructura (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recurso TEXT NOT NULL,
            estado TEXT NOT NULL,
            costo_mantenimiento REAL
        )
    ''')
    # Crear tabla para tareas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT NOT NULL,
            asignado_a TEXT NOT NULL,
            estado TEXT NOT NULL,
            fecha_limite TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Llamar a la función para inicializar la base de datos
init_db()

@app.route('/')
def home():
    return render_template('index.html')

# Ruta para agregar empleado
@app.route('/agregar_empleado', methods=['POST'])
def agregar_empleado():
    nombre = request.form.get('nombre')
    puesto = request.form.get('puesto')
    horas_trabajadas = request.form.get('horas_trabajadas')
    eficiencia = request.form.get('eficiencia')

    if nombre and puesto and horas_trabajadas and eficiencia:
        conn = sqlite3.connect('gestion_recursos.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO empleados (nombre, puesto, horas_trabajadas, eficiencia)
            VALUES (?, ?, ?, ?)
        ''', (nombre, puesto, int(horas_trabajadas), float(eficiencia)))
        conn.commit()
        conn.close()
    return redirect(url_for('home'))

# Ruta para agregar recurso
@app.route('/agregar_recurso', methods=['POST'])
def agregar_recurso():
    recurso = request.form.get('recurso')
    estado = request.form.get('estado')
    costo_mantenimiento = request.form.get('costo_mantenimiento')

    if recurso and estado and costo_mantenimiento:
        conn = sqlite3.connect('gestion_recursos.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO infraestructura (recurso, estado, costo_mantenimiento)
            VALUES (?, ?, ?)
        ''', (recurso, estado, float(costo_mantenimiento)))
        conn.commit()
        conn.close()
    return redirect(url_for('home'))

# Ruta para agregar tarea
@app.route('/agregar_tarea', methods=['POST'])
def agregar_tarea():
    descripcion = request.form.get('descripcion')
    asignado_a = request.form.get('asignado_a')
    estado = request.form.get('estado')
    fecha_limite = request.form.get('fecha_limite')

    if descripcion and asignado_a and estado and fecha_limite:
        conn = sqlite3.connect('gestion_recursos.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tareas (descripcion, asignado_a, estado, fecha_limite)
            VALUES (?, ?, ?, ?)
        ''', (descripcion, asignado_a, estado, fecha_limite))
        conn.commit()
        conn.close()
    return redirect(url_for('home'))

# Ruta para ver empleados
@app.route('/empleados')
def ver_empleados():
    conn = sqlite3.connect('gestion_recursos.db')
    empleados_df = pd.read_sql_query('SELECT * FROM empleados', conn)
    conn.close()
    return render_template('empleados.html', empleados=empleados_df.to_dict(orient='records'))

# Ruta para ver recursos
@app.route('/recursos')
def ver_recursos():
    conn = sqlite3.connect('gestion_recursos.db')
    recursos_df = pd.read_sql_query('SELECT * FROM infraestructura', conn)
    conn.close()
    return render_template('recursos.html', recursos=recursos_df.to_dict(orient='records'))

# Ruta para ver tareas
@app.route('/tareas')
def ver_tareas():
    conn = sqlite3.connect('gestion_recursos.db')
    tareas_df = pd.read_sql_query('SELECT * FROM tareas', conn)
    conn.close()
    return render_template('tareas.html', tareas=tareas_df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)