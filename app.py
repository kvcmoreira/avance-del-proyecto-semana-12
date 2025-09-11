from flask import Flask, render_template, request, redirect, url_for, flash
import json
import csv
import os
from datetime import datetime
from Conexión.conexión import obtener_conexion

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_123'  # Cambia esto por algo más seguro

# Directorios
DATA_DIR = 'datos'
DB_PATH = 'database/usuarios.db'
cn=obtener_conexion
# Asegurarse de que los directorios existan
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs('database', exist_ok=True)

# --- FUNCIONES PARA ARCHIVOS ---
def guardar_en_txt(producto):
    with open(os.path.join(DATA_DIR, 'datos.txt'), 'a') as f:
        f.write(f"{producto['nombre']},{producto['cantidad']},{producto['precio']}\n")

def leer_txt():
    productos = []
    if os.path.exists(os.path.join(DATA_DIR, 'datos.txt')):
        with open(os.path.join(DATA_DIR, 'datos.txt'), 'r') as f:
            for linea in f:
                partes = linea.strip().split(',')
                if len(partes) == 3:
                    productos.append({
                        'id': len(productos) + 1,
                        'nombre': partes[0],
                        'cantidad': int(partes[1]),
                        'precio': float(partes[2])
                    })
    return productos

def guardar_en_json(producto):
    filename = os.path.join(DATA_DIR, 'datos.json')
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            data = json.load(f)
    else:
        data = []

    data.append(producto)
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def leer_json():
    filename = os.path.join(DATA_DIR, 'datos.json')
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return []

def guardar_en_csv(producto):
    filename = os.path.join(DATA_DIR, 'datos.csv')
    with open(filename, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([producto['nombre'], producto['cantidad'], producto['precio']])

def leer_csv():
    productos = []
    filename = os.path.join(DATA_DIR, 'datos.csv')
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 3:
                    productos.append({
                        'id': len(productos) + 1,
                        'nombre': row[0],
                        'cantidad': int(row[1]),
                        'precio': float(row[2])
                    })
    return productos

# --- MODELO DE DATOS SQLITE ---
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Producto(Base):
    __tablename__ = 'productos'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio = Column(Float, nullable=False)

engine = create_engine(f'sqlite:///{DB_PATH}')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# --- RUTAS ---
@app.route('/')
def index():
    session = Session()
    productos_db = session.query(Producto).all()
    session.close()
    return render_template('index.html', productos=productos_db)

@app.route('/añadir', methods=['GET', 'POST'])
def añadir():
    if request.method == 'POST':
        nombre = request.form['nombre']
        cantidad = int(request.form['cantidad'])
        precio = float(request.form['precio'])

        producto = {
            'nombre': nombre,
            'cantidad': cantidad,
            'precio': precio
        }

        # Guardar en todos los formatos
        guardar_en_txt(producto)
        guardar_en_json(producto)
        guardar_en_csv(producto)

        # Guardar en SQLite
        session = Session()
        nuevo_producto = Producto(nombre=nombre, cantidad=cantidad, precio=precio)
        session.add(nuevo_producto)
        session.commit()
        session.close()

        flash("Producto agregado correctamente")
        return redirect(url_for('index'))

    return render_template('formulario.html')

@app.route('/eliminar/<int:id>')
def eliminar(id):
    session = Session()
    producto = session.query(Producto).filter_by(id=id).first()
    if producto:
        session.delete(producto)
        session.commit()
        flash("Producto eliminado")
    session.close()
    return redirect(url_for('index'))

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    session = Session()
    producto = session.query(Producto).filter_by(id=id).first()
    if not producto:
        flash("Producto no encontrado")
        return redirect(url_for('index'))

    if request.method == 'POST':
        producto.nombre = request.form['nombre']
        producto.cantidad = int(request.form['cantidad'])
        producto.precio = float(request.form['precio'])
        session.commit()
        flash("Producto actualizado")
        session.close()
        return redirect(url_for('index'))

    session.close()
    return render_template('formulario.html', producto=producto)

@app.route('/ver-txt')
def ver_txt():
    productos = leer_txt()
    return render_template('resultado.html', productos=productos, tipo='TXT')

@app.route('/ver-json')
def ver_json():
    productos = leer_json()
    return render_template('resultado.html', productos=productos, tipo='JSON')

@app.route('/ver-csv')
def ver_csv():
    productos = leer_csv()
    return render_template('resultado.html', productos=productos, tipo='CSV')





if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)