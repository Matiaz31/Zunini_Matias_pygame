import pygame
from Codigo_Assets import (ALTO_VENTANA, ANCHO_VENTANA)
from Codigo_Auxi import (open_configs)

class Agujero(pygame.sprite.Sprite):
    def __init__(self, diccionario):
        self.__configs = open_configs().get("config_mundo")
        self.__fosa = pygame.image.load(self.__configs["fosa"])
        self.__fosa_rect = self.__fosa.get_rect()

    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self.__fosa, self.__fosa_rect)

    @property
    def get_rect(self):
        return self.__fosa_rect