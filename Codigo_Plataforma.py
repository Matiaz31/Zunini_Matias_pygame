import pygame, random
from Codigo_Assets import (ALTO_VENTANA, ANCHO_VENTANA)
from Codigo_Auxi import (open_configs)

class Agujero(pygame.sprite.Sprite):
    def __init__(self, diccionario):
        super().__init__()
        self.__configs = open_configs().get("config_mundo")
        self.__fosa = pygame.transform.scale(pygame.image.load(self.__configs["fosa"]),(140,150))
        self.__fosa_rect = self.__fosa.get_rect()

        self.__fosa_rect.x = random.randint(120, 400)
        self.__fosa_rect.y = random.randint(80, 500)

    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self.__fosa, self.__fosa_rect)

    def update(self, screen: pygame.surface.Surface):
        self.draw(screen)

    def get_rect(self):
        return self.__fosa_rect