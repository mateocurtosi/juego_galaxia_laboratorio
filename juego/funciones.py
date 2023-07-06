import pygame
import sqlite3
from clases import *
from funciones import *
from sonidos_imagenes import *
from sql import *

ANCHO = 1200
ALTO = 600
NEGRO = (0, 0, 0)

clock = pygame.time.Clock()

screen = pygame.display.set_mode((ANCHO, ALTO))
# FUNCION PARA DIBUJAR TEXTO
def dibujar_texto(surface, text, size, x, y):
    font = pygame.font.SysFont("serif", size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


# FUNCION PARA DIBUJAR BARRA SALUD
def dibujar_barra_salud(surface, x, y, percentage):
    BAR_LENGTH = 150
    BAR_HEIGHT = 10
    fill = (percentage / 100) * BAR_LENGTH
    border = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, (0, 255, 0), fill)
    pygame.draw.rect(surface, (255, 255, 255), border, 2)


# Reinicia el juego, elimina todos los sprites, crea 6 meteoros y retorna un jugador
# def reiniciar_juego():
#     all_sprites.empty()
#     meteors.empty()
#     bullets.empty()
#     explosions.empty()

#     jugador = Jugador()
#     all_sprites.add(jugador)

#     for i in range(6):
#         meteoro = Meteoro()
#         all_sprites.add(meteoro)
#         meteors.add(meteoro)
#     return jugador


# Conectar con la base de datos
DB_FILE = 'puntajes.db'
try:
    conexion = sqlite3.connect(DB_FILE)
    print("Conexión exitosa a la base de datos")
except sqlite3.Error as error:
    print("Error al conectar a la base de datos:", error)


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


# Se conecta a la base de datos, crea un cursor y ejecuta una consulta SQL para obtener los mejores 10 puntajes de la tabla "puntajes"
def obtener_mejores_puntajes(top_n):
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT nombre, puntaje FROM puntajes ORDER BY puntaje DESC LIMIT ?", (top_n,))
        mejores_puntuaciones = c.fetchall()
        conn.close()
        return mejores_puntuaciones
    except sqlite3.Error as error:
        print("Error al obtener los puntajes:", error)

def Pantalla_game_over(score,tiempo_final,nombre):
    screen.fill(NEGRO)
    dibujar_texto(screen, "Juego Terminado.", 75, ANCHO // 2, ALTO // 7)
    dibujar_texto(screen, "Tu nave fue destruida", 60, ANCHO // 2, ALTO // 3.9)
    dibujar_texto(screen, f"Puntaje obtenido: {score}", 27, ANCHO // 2, ALTO // 2.7)
    dibujar_texto(screen, f"Tiempo de juego: {tiempo_final // 60} segundos", 27, ANCHO // 2, ALTO // 2.4)
    dibujar_texto(screen, "Presiona la letra 'X' para empezar a guardar tu puntuación junto a 3 iniciales", 27, ANCHO // 2, ALTO // 2.1)
    dibujar_texto(screen, "Escribe 3 letras y luego vuelve a presionar 'X' para confirmarlo", 27, ANCHO // 2, ALTO // 1.9)
    dibujar_texto(screen, f"Nombre: {nombre}", 27, ANCHO // 2, ALTO // 1.7)
    dibujar_texto(screen, " TOP 5 Mejores Puntuaciones:", 27, ANCHO // 2, ALTO // 1.5)
    
    mejores_puntuaciones = obtener_mejores_puntajes(5)
    
    y_offset = ALTO // 1.4
    for i, (nombre_puntuacion, puntaje) in enumerate(mejores_puntuaciones):
        texto_puntuacion = f"{nombre_puntuacion}: {puntaje}"
        dibujar_texto(screen, texto_puntuacion, 27, ANCHO // 2, y_offset)
        y_offset += 30  # Aumentar el offset vertical para la siguiente puntuación 

    pygame.display.flip()        

#PANTALLA DE INICIO
def Pantalla_inicio():
    dibujar_texto(screen, "LLUVIA DE METEORITOS", 65, ANCHO // 2, ALTO // 4)
    dibujar_texto(screen, "Tu objetivo es destruir el mayor número de meteoritos. Solo podrás recibir 4 impactos.", 27,ANCHO // 2, ALTO // 2)
    dibujar_texto(screen, "Presiona cualquier tecla para jugar", 30, ANCHO // 2, ALTO * 3 / 4)
    pygame.display.flip()
    #Espera que se toque una tecla para salir o que se cierre el juego
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


all_sprites = pygame.sprite.Group()#se crea el grupo de todos los sprites
meteors = pygame.sprite.Group()# grupo para almacenar los meteoros
bullets = pygame.sprite.Group()# grupo para alacenar los sprites de las balas
explosions = pygame.sprite.Group()# grupo para almacenar los sprites de las explosiones
jugador = Jugador()#se crea instancia de jugador
all_sprites.add(jugador)#se agrega al grupo all_sprites



#VARIABLES
tiempo = 0
score = 0
nivel = 1
running = True
game_over = False
nombre = ""



# Función para obtener el nombre del usuario después de presionar la tecla "X"
def obtener_nombre_usuario():
    nombre = ""
    ingresando_nombre = True
    while ingresando_nombre:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    ingresando_nombre = False
                elif event.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                else:
                    if event.unicode.isalnum():
                        nombre += event.unicode
    
    return nombre[:3]

def estadisticas():
    # Barra de salud
        dibujar_texto(screen, "Salud de la nave", 20, 80, 18)
        dibujar_barra_salud(screen, 5, 5, jugador.shield)
        # Puntaje
        dibujar_texto(screen, f"Puntaje: {score}", 20, ANCHO // 2, 10)
        # Nivel
        dibujar_texto(screen, f"Nivel: {nivel}", 20, ANCHO - 50, 10)