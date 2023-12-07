import pygame
from Codigo_Assets import (ALTO_VENTANA, ANCHO_VENTANA)

class Fruta(pygame.sprite.Sprite):
    def __init__(self, diccionario, coord_x, coord_y, item: str):
        super().__init__()
        self.__mundo_config = diccionario.get("config_mundo")
        self.__gema_img = pygame.transform.scale(pygame.image.load(self.__mundo_config["gema"]),(25,25))
        self.__heart_img = pygame.transform.scale(pygame.image.load(self.__mundo_config["heart"]),(25,25))

        self.__rect_gema = self.__gema_img.get_rect()
        self.__rect_hert = self.__heart_img.get_rect()

        self.__rect_gema.x = coord_x
        self.__rect_gema.y = coord_y

        self.__rect_hert.x = coord_x
        self.__rect_hert.y = coord_y

        self.__item = item

        match self.__item:
            case "gema":
                self.rect = self.__gema_img.get_rect()
            case "heart":
                self.rect = self.__heart_img.get_rect()

    def draw(self, screen: pygame.surface.Surface):
        match self.__item:
            case "gema":
                screen.blit(self.__gema_img, self.__rect_gema)
            case "heart":
                screen.blit(self.__heart_img, self.__rect_hert)

    def update(self, screen: pygame.surface.Surface):
        self.draw(screen)