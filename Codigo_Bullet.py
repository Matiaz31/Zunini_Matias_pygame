import pygame
from Codigo_Auxi import (move_coords)
from Codigo_Assets import (ANCHO_VENTANA, ALTO_VENTANA)

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x, y, direccion:str=""):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("Renders\energi_ball.png").convert(),(30,30))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.centerx = x
        self.direccion = direccion

    def update(self):
        match self.direccion:
            case "Right-Up":
                self.rect.x += 10
                self.rect.y -= 10
                if self.rect.x >= ANCHO_VENTANA:
                    self.kill()
            case "Left-Down":
                self.rect.x -= 10
                self.rect.y += 10
                if self.rect.x <= 0:
                    self.kill()
            case "Right-Down":
                self.rect.x += 10
                self.rect.y += 10
                if self.rect.x >= ANCHO_VENTANA:
                    self.kill()
            case "Left-Up":
                self.rect.x -= 10
                self.rect.y -= 10
                if self.rect.x <= 0:
                    self.kill()
