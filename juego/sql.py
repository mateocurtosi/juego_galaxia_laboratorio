import sqlite3

# Conectar con la base de datos
DB_FILE = 'puntajes.db'
try:
    conexion = sqlite3.connect(DB_FILE)
    print("Conexión exitosa a la base de datos")
except sqlite3.Error as error:
    print("Error al conectar a la base de datos:", error)

# Crear la tabla "puntajes"
try:
    cursor = conexion.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS puntajes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT,
                        puntaje INTEGER
                    )''')
    conexion.commit()
    print("Tabla creada exitosamente o ya existente")
except sqlite3.Error as error:
    print("Error al crear la tabla:", error)    

# Se conecta a la base de datos, crea un cursor y ejecuta una consulta SQL para insertar el nombre y puntaje en la tabla "puntajes"
def guardar_puntaje(nombre, puntaje):
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("INSERT INTO puntajes (nombre, puntaje) VALUES (?, ?)", (nombre, puntaje))
        conn.commit()
        conn.close()
        print("Puntaje guardado exitosamente")
    except sqlite3.Error as error:
        print("Error al guardar el puntaje:", error)


# FUNCION PARA OBTENER LOS MEJORES PUNTAJES DE LA BASE DE DATOS
# Se conecta a la base de datos, crea un cursor y ejecuta una consulta SQL para seleccionar los nombres y puntajes de la tabla puntajes ordenados por puntaje descendente
def obtener_mejores_puntajes(limit=5):
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT nombre, puntaje FROM puntajes ORDER BY puntaje DESC LIMIT ?", (limit,))
        puntajes = c.fetchall()
        conn.close()
        print("Puntajes obtenidos exitosamente")
        return puntajes
    except sqlite3.Error as error:
        print("Error al obtener los puntajes:", error)