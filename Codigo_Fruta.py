import pygame
from Codigo_Assets import (ALTO_VENTANA, ANCHO_VENTANA)

class Fruta(pygame.sprite.Sprite):
    def __init__(self, diccionario, coord_x, coord_y, item: str):
        super().__init__()
        self.__mundo_config = diccionario.get("config_mundo")
        self.__gema_img = pygame.transform.scale(pygame.image.load(self.__mundo_config["gema"]),(45,45))
        self.__heart_img = pygame.transform.scale(pygame.image.load(self.__mundo_config["heart"]),(45,45))

        self.__item = item
        match self.__item:
            case "gema":
                self.rect = self.__gema_img.get_rect()
            case "heart":
                self.rect = self.__heart_img.get_rect()

        self.rect.x = coord_x
        self.rect.y = coord_y

    def draw(self, screen: pygame.surface.Surface):
        match self.__item:
            case "gema":
                screen.blit(self.__gema_img, self.rect)
            case "heart":
                screen.blit(self.__heart_img, self.rect)

    def update(self, screen: pygame.surface.Surface):
        self.draw(screen)