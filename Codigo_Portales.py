import pygame
from Codigo_Assets import (ALTO_VENTANA, ANCHO_VENTANA)

class Portales():
    def __init__(self, diccionario,coord_x,coord_y):
        self.__mundo_config = diccionario.get("config_mundo")
        self.__portal_on_img = pygame.image.load(self.__mundo_config["portal_on"])
        self.__portal_off_img = pygame.image.load(self.__mundo_config["portal_off"])

        self.__cordenadas_1 = (20,20)
        self.__cordenadas_2 = (ANCHO_VENTANA-self.rect_1.width-20, ALTO_VENTANA-self.rect_1.height-20)

        self.on = False
        self.off = True

        if self.on:
            self.rect = self.__portal_on_img.get_rect()
        elif self.off:
            self.rect = self.__portal_off_img.get_rect()


        self.rect.x = coord_x
        self.rect.y = coord_y

    def draw(self, screen: pygame.surface.Surface):
        if self.on:
            screen.blit(self.__portal_on_img, self.rect)
        elif self.off:
            screen.blit(self.__portal_off_img, self.rect)

    def update(self, screen: pygame.surface.Surface):
        self.draw(screen)