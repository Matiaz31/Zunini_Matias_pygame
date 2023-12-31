import pygame
from Codigo_Auxi import (move_coords)
from Codigo_Assets import (ANCHO_VENTANA, ALTO_VENTANA)

class Bala(pygame.sprite.Sprite):
    def __init__(self,x, y, img, direccion:str=""):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(img).convert(),(30,30))
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

            case "cono_1":
                pass
            case "cono_2":
                pass
            case "cono_3":
                pass

class Flecha(pygame.sprite.Sprite):
    def __init__(self,x, y, img, direccion:str=""):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(img).convert(),(30,30))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.centerx = x
        self.direccion = direccion

    def update(self):
        match self.direccion:
            case "Right":
                self.rect.x += 6
            case "Left":
                self.rect.x -= 6