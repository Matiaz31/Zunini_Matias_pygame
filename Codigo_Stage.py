import pygame
from Codigo_Hero import Hero
from Codigo_Enemys import Zambie,Fantasma
from Codigo_Auxi import (open_configs)

class Stage:
    def __init__(self, screen: pygame.surface.Surface, limit_w, limit_h, dificultad: str):
        self.__configs = open_configs()
        self.player_sprite = Hero(50, 8, self.__configs)
        self.enemies = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle(self.player_sprite)
        self.dificultad = dificultad
        self.__mapa_config = self.__configs.get("config_mundo")
        self.__dificulty_config = self.__configs.get(self.dificultad)
        self.__enemis_config = self.__dificulty_config.get("enemigos")
        self.__max_enemies = self.__enemis_config["cantidad"]
        self.__player_win = False
        self.__limit_w = limit_w
        self.__limit_h = limit_h
        self.__main_screen = screen
        self.fondo = pygame.image.load(self.__mapa_config["fondo"]).convert_alpha()

        self.enemies_class = []
        self.spawnear_enemigos()

        for enemy in self.enemies_class:
            self.enemies.add(enemy)

    def spawnear_enemigos(self):
        for _ in range(self.__max_enemies):
            zambie = Zambie(100,self.player_sprite.get_rect, self.__enemis_config)
            fantom = Fantasma(100, self.__enemis_config)
            zambie.enemigos.append(zambie)
            self.enemies.add(fantom)
            self.enemies.add(zambie)

    def run(self, delta_ms):
        self.enemies.update(delta_ms, self.__main_screen)
        self.player_sprite.update(delta_ms, self.__main_screen)
        self.player_sprite.draw(self.__main_screen)

        for bullet in self.player_sprite.get_bullets:
            cantidad_antes = len(self.enemies)
            pygame.sprite.spritecollide(bullet, self.enemies, True)
            cantidad_despues = len(self.enemies)
            if cantidad_antes > cantidad_despues:
                bullet.kill()
                cantidad_vencido = cantidad_antes - cantidad_despues
                self.player_sprite.puntaje += cantidad_vencido * 60
                print(f'Puntaje actual: {self.player_sprite.puntaje} Puntos')
            if len(self.enemies) == 0 and not self.__player_win:
                self.__player_win = True
                print(f'Ganaste la partida con: {self.player_sprite.puntaje} Puntos!')