import sqlite3

SENSORS_TABLE = "sensors_sensor"
conexion = sqlite3.connect('db.sqlite3')

# Crear un cursor para ejecutar consultas
cursor = conexion.cursor()

# Ejecutar una consulta SELECT para obtener todas las filas de la tabla
cursor.execute(f"SELECT * FROM {SENSORS_TABLE}")

# Obtener los nombres de las columnas de la tabla
nombres_columnas = [descripcion[0] for descripcion in cursor.description]

# Imprimir los nombres de las columnas
for nombre_columna in nombres_columnas:
    print(nombre_columna, end='\t')
print()

# Imprimir los valores de cada fila
for fila in cursor.fetchall():
    for valor in fila:
        print(valor, end='\t')
    print()

# Cerrar la conexión a la base de datos
conexion.close()
