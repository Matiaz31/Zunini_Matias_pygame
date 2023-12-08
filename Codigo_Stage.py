import pygame
import random
from Codigo_Hero import Hero
from Codigo_Enemys import Zambie,Fantasma
from Codigo_Fruta import Fruta
from Codigo_Plataforma import Agujero
from Codigo_Auxi import (open_configs, play_music)

class Stage:
    def __init__(self, screen: pygame.surface.Surface, limit_w, limit_h, dificultad: str):
        self.__configs = open_configs()
        self.player_sprite = Hero(50,self.__configs)
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
        self.frutas = pygame.sprite.Group()
        self.fondo = pygame.image.load(self.__mapa_config["fondo"]).convert_alpha()
        self.fosa = Agujero(self.__configs, 130, 200)
        self.__is_hitting = False
        self.__is_inmortal = False
        self.perdiste = False
        self.__tiempo = 0

        #self.enemies_hit = False
        self.all_enemies = []
        self.spawnear_enemigos(self.__max_enemies)

        # for enemy in self.enemies_class:
        #     self.enemies.add(enemy)

    def run(self, delta_ms):
        self.fosa.update(self.__main_screen)
        self.frutas.update(self.__main_screen)
        self.enemies.update(delta_ms, self.__main_screen)
        self.player_sprite.update(delta_ms, self.__main_screen)
        #self.player_sprite.draw(self.__main_screen)
        self.check_colide()
        #self.__configs.update()

    def cargar_nuevas_configs(self, dificultad):
        self.dificultad = dificultad
        self.__configs = open_configs()
        self.__mapa_config = self.__configs.get("config_mundo")
        self.__dificulty_config = self.__configs.get(self.dificultad)
        self.__enemis_config = self.__dificulty_config.get("enemigos")
        self.__max_enemies = self.__enemis_config["cantidad"]

    def get_tiempo(self):
        return pygame.time.get_ticks()//1000

    def spawnear_enemigos(self, cantidad):
        for _ in range(cantidad):
            zambie = Zambie(100,self.player_sprite.rect, self.__enemis_config)
            fantom = Fantasma(100,self.player_sprite.rect, self.__enemis_config)

            self.enemies.add(fantom)
            self.enemies.add(zambie)
            self.all_enemies.append(fantom)
            self.all_enemies.append(zambie)

    def create_enemigos(self, cantidad):
        for _ in range(cantidad):
            eleccion = random.randint(1,2)
            if eleccion == 1:
                zambie = Zambie(100,self.player_sprite.rect, self.__enemis_config)
                self.enemies.add(zambie)
            else:
                fantom = Fantasma(100,self.player_sprite.rect, self.__enemis_config)
                self.enemies.add(fantom)

    def check_colide(self):
        if pygame.sprite.spritecollideany(self.player_sprite, self.enemies):
            self.__is_hitting = True
            self.chek_hero_life()
            self.inmortal()
        else:
            self.__is_hitting = False
            self.inmortal()
        if pygame.sprite.spritecollide(self.player_sprite, self.frutas, True):
            self.player_sprite.puntaje += 20
        
        for bullet in self.player_sprite.get_bullets:
            cantidad_antes = len(self.enemies)
            for enemi in self.enemies:
                if pygame.sprite.collide_rect(bullet, enemi):
                    bullet.kill()
                    enemi.vida -= self.player_sprite.daño_bala
                    self.check_enemi_death()
            cantidad_despues = len(self.enemies)
            
        for flecha in self.player_sprite.get_flechas:
            cantidad_antes = len(self.enemies)
            for enemi in self.enemies:
                if pygame.sprite.collide_rect(flecha, enemi):
                    enemi.vida -= self.player_sprite.daño_flecha
                    self.check_enemi_death()
            cantidad_despues = len(self.enemies)


            if cantidad_antes > cantidad_despues:
                cantidad_vencido = cantidad_antes - cantidad_despues
                self.player_sprite.puntaje += cantidad_vencido * 60
                print(f'Puntaje actual: {self.player_sprite.puntaje} Puntos')
            # if len(self.enemies) == 0 and not self.__player_win:
            #     self.__player_win = True
            #     print(f'Ganaste la partida con: {self.player_sprite.__puntaje} Puntos!')

        if len(self.enemies) < len(self.all_enemies):
            cantidad = len(self.all_enemies) - len(self.enemies)
            self.create_enemigos(cantidad)
                    
    def chek_hero_life(self):
        if not self.__is_inmortal:
            self.player_sprite.vida -= 100
            if self.player_sprite.vida <= 0:
                self.perdiste = True
    
    def inmortal(self):
        if self.__is_hitting:
            self.__is_inmortal = True
        if not self.__is_hitting:
            self.__is_inmortal = False

    def check_enemi_death(self):
        for enemi in self.enemies:     
            if enemi.vida <= 0:
                self.player_sprite.puntaje += 130
                pos_x = enemi.rect.x
                pos_y = enemi.rect.y
                self.frutas.add(Fruta(self.__configs,pos_x,pos_y, "gema"))
                enemi.kill()

    