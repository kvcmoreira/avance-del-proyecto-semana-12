from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from conexion.conexion import obtener_conexion   # tu conexión existente
from forms import ProductoForm
from models import User  # el modelo de usuario que creamos antes
import mysql.connector

app = Flask(__name__)
app.secret_key = "clave_secreta"

# -------------------------
# Configurar Flask-Login
# -------------------------
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (user_id,))
    data = cursor.fetchone()
    conexion.close()
    if data:
        return User(data['id_usuario'], data['nombre'], data['email'], data['password'])
    return None

# -------------------------
# Rutas de Login / Registro
# -------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        password = request.form["password"]

        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, email, password) VALUES (%s,%s,%s)", (nombre,email,password))
        conexion.commit()
        conexion.close()
        flash("Usuario registrado con éxito")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE email = %s AND password = %s", (email,password))
        data = cursor.fetchone()
        conexion.close()

        if data:
            user = User(data['id_usuario'], data['nombre'], data['email'], data['password'])
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            flash("Usuario o contraseña incorrectos")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)

# -------------------------
# Rutas de Productos
# -------------------------
@app.route("/")
def index():
    return render_template("index.html", user=current_user)

@app.route("/formulario", methods=["GET", "POST"])
@login_required  # proteger para que solo usuarios logueados puedan agregar productos
def formulario():
    form = ProductoForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        cantidad = form.cantidad.data
        precio = form.precio.data

        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO productos (nombre, cantidad, precio) VALUES (%s, %s, %s)",
            (nombre, cantidad, precio)
        )
        conexion.commit()
        cursor.close()
        conexion.close()

        return redirect(url_for("resultado", nombre=nombre, cantidad=cantidad, precio=precio))
    return render_template("formulario.html", form=form)

@app.route("/resultado")
@login_required
def resultado():
    nombre = request.args.get("nombre")
    cantidad = request.args.get("cantidad")
    precio = request.args.get("precio")
    return render_template("resultado.html", nombre=nombre, cantidad=cantidad, precio=precio)

@app.route("/lista")
@login_required
def lista():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return render_template("lista.html", productos=productos)

# Ruta de prueba para la conexión MySQL
@app.route("/test_db")
def test_db():
    try:
        conexion = obtener_conexion()
        if conexion.is_connected():
            return "✅ Conexión a MySQL exitosa!"
    except Exception as e:
        return f"❌ Error de conexión: {e}"

# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
