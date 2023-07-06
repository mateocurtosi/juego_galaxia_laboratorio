import pygame


ANCHO = 1200
ALTO = 600

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Galaxia")
clock = pygame.time.Clock()

laser_sound = pygame.mixer.Sound("sonidos\laser5.ogg")
explosion_sound = pygame.mixer.Sound("sonidos\explosion.wav")
musica_fondo = pygame.mixer.Sound("sonidos\musica_juego.mp3")
#pygame.mixer.music.set_volume(0.0)
#musica_fondo.play(-1)

#CARGAR IMAGENES METEOROS
meteor_imagenes = []
meteor_list = [
    "imagenes/asteroide.png",
    "imagenes/asteroide1.png",
    "imagenes/asteroide2.png",
]
for img in meteor_list:
    meteor_imagenes.append(pygame.image.load(img).convert())

#ESTABLECER FONDO DE PANTALLA
background = pygame.image.load("imagenes/fondo_pantalla.jpg").convert()