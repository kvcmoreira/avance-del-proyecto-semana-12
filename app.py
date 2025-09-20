from flask import Flask, render_template, request, redirect, url_for
from conexion.conexion import obtener_conexion   # ✅ ahora importa desde la carpeta conexion
from forms import ProductoForm

app = Flask(__name__)
app.secret_key = "clave_secreta"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/formulario", methods=["GET", "POST"])
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
def resultado():
    nombre = request.args.get("nombre")
    cantidad = request.args.get("cantidad")
    precio = request.args.get("precio")
    return render_template("resultado.html", nombre=nombre, cantidad=cantidad, precio=precio)

@app.route("/lista")
def lista():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return render_template("lista.html", productos=productos)

# 🚀 Ruta de prueba para verificar la conexión con MySQL
@app.route("/test_db")
def test_db():
    try:
        conexion = obtener_conexion()
        if conexion.is_connected():
            return "✅ Conexión a MySQL exitosa!"
    except Exception as e:
        return f"❌ Error de conexión: {e}"

if __name__ == "__main__":
    app.run(debug=True)
