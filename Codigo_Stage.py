import pygame
from Codigo_Auxi import (open_configs)

class Stage:
    def __init__(self, screen: pygame.surface.Surface, limit_w, limit_h, config: str):
        self.__configs = open_configs().get(config)
        