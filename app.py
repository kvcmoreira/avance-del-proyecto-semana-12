from flask import Flask

app = Flask(__name__)
from flask import Flask

app = Flask(__name__)

@app.route("/")  # Esta es la ruta raíz
def home():
    return "¡Hola! Flask está funcionando."

from conexion.conexion import obtener_conexion

conexion = obtener_conexion()

if conexion:
    cursor = conexion.cursor()

    sql = "INSERT INTO productos (nombre_producto, cantidad, precio, fecha) VALUES (%s, %s, %s, %s)"
    valores = ("Taladro", 10, 120.00, "2025-09-19")

    cursor.execute(sql, valores)
    conexion.commit()

    print(cursor.rowcount, "producto agregado.")

    cursor.close()
    conexion.close()

