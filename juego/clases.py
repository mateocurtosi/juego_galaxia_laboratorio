import pygame
import random
from sonidos_imagenes import *


ANCHO = 1200
ALTO = 600
NEGRO = (0, 0, 0)

# CLASES
class Proyectil(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("imagenes\disparo.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image.set_colorkey(NEGRO)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x
        self.speedy = -10

    #desplaza el proyectil y lo elimina si supera la parte superior
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("imagenes/nave.png").convert()
        self.image.set_colorkey(NEGRO)
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.bottom = ALTO - 10
        self.speed_x = 0
        self.shield = 100

    #Permite el movimiento y delimita para que no salga de la pantalla
    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x

        if self.rect.right > ANCHO:
            self.rect.right = ANCHO
        if self.rect.left < 0:
            self.rect.left = 0

    #Crea el proyectil en la posicion del jugador y lo agrega a grupos de sprite y reproduce sonido
    def shoot(self):
        bullet = Proyectil(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        laser_sound.play()


class Meteoro(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(meteor_imagenes)
        self.image.set_colorkey(NEGRO)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ANCHO - self.rect.width)
        self.rect.y = random.randrange(-140, -100)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-5, 5)

    #Actualiza la posicion del meteoro y si se sale de pantalla lo vuelve a generar
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > ALTO + 10 or self.rect.left < -100 or self.rect.right > ANCHO + 100:
            self.rect.x = random.randrange(ANCHO - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 10)

    #Crea una explosion en la posicion del meteoro y agrega a los grupos correspondientes
    def explode(self):
        explosion = Explosion(self.rect.center)
        all_sprites.add(explosion)
        explosions.add(explosion)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load("imagenes\explosion.png")
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.frame = 0
        self.animation = 10

    #Actualiza la animacion de la explocion y la elimina cuando se completa
    def update(self):
        self.frame += 1
        if self.frame == self.animation:
            self.kill()

all_sprites = pygame.sprite.Group()#se crea el grupo de todos los sprites
meteors = pygame.sprite.Group()# grupo para almacenar los meteoros
bullets = pygame.sprite.Group()# grupo para alacenar los sprites de las balas
explosions = pygame.sprite.Group()# grupo para almacenar los sprites de las explosiones
jugador = Jugador()#se crea instancia de jugador
all_sprites.add(jugador)#se agrega al grupo all_sprites