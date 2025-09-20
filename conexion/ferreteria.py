import mysql.connector

def conectar():
    """Conectar a la base de datos ferreteria"""
    return mysql.connector.connect(
        host="localhost",
        user="root",          # tu usuario de phpMyAdmin
        password="",          # tu contraseña, si tienes deja aquí
        database="ferreteria"
    )

def listar_productos():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    print("\n--- LISTA DE PRODUCTOS ---")
    for p in productos:
        print(f"ID: {p[0]}, Nombre: {p[1]}, Cantidad: {p[2]}, Precio: {p[3]}, Fecha: {p[4]}")
    conexion.close()

def agregar_producto(nombre, cantidad, precio, fecha):
    conexion = conectar()
    cursor = conexion.cursor()
    sql = "INSERT INTO productos (nombre_producto, cantidad, precio, fecha) VALUES (%s, %s, %s, %s)"
    valores = (nombre, cantidad, precio, fecha)
    cursor.execute(sql, valores)
    conexion.commit()
    print(f"\nProducto '{nombre}' agregado correctamente.")
    conexion.close()

def actualizar_producto(id_producto, cantidad=None, precio=None):
    conexion = conectar()
    cursor = conexion.cursor()
    if cantidad is not None:
        cursor.execute("UPDATE productos SET cantidad=%s WHERE id=%s", (cantidad, id_producto))
    if precio is not None:
        cursor.execute("UPDATE productos SET precio=%s WHERE id=%s", (precio, id_producto))
    conexion.commit()
    print(f"\nProducto con ID {id_producto} actualizado.")
    conexion.close()

def eliminar_producto(id_producto):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM productos WHERE id=%s", (id_producto,))
    conexion.commit()
    print(f"\nProducto con ID {id_producto} eliminado.")
    conexion.close()

# --- EJEMPLO DE USO ---
if __name__ == "__main__":
    listar_productos()                  # Muestra todos los productos
    agregar_producto("Martillo", 15, 18.50, "2025-09-19")   # Agrega un producto
    actualizar_producto(1, cantidad=50)                      # Actualiza cantidad del producto con ID=1
    eliminar_producto(2)                                     # Elimina el producto con ID=2
    listar_productos()                  # Lista productos nuevamente
