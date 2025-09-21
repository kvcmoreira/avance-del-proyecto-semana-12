import mysql.connector

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",          # usuario de phpMyAdmin
            password="",          # tu contraseña de MySQL (vacía si no pusiste)
            database="ferreteria" # tu base de datos
        )
        if conexion.is_connected():
            print("✅ Conexión exitosa a la base de datos")
        return conexion
    except mysql.connector.Error as err:
        print("❌ Error al conectar:", err)
        return None
