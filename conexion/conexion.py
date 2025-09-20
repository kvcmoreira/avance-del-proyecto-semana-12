import mysql.connector

try:
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ferreteria"
    )

    cursor = conexion.cursor()

    sql = "INSERT INTO productos (nombre_producto, cantidad, precio, fecha) VALUES (%s, %s, %s, %s)"
    valores = ("Taladro", 10, 120.00, "2025-09-19")
    cursor.execute(sql, valores)

    conexion.commit()
    print(cursor.rowcount, "producto agregado.")

except mysql.connector.Error as err:
    print("Error:", err)

finally:
    if conexion.is_connected():
        conexion.close()
