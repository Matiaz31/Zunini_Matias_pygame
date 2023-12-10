import pygame
import random
from Codigo_Hero import Hero
from Codigo_Enemys import Zambie,Fantasma,Trampa
from Codigo_Fruta import Fruta
from Codigo_Plataforma import Agujero
from Codigo_Auxi import (open_configs, play_music)

class Stage:
    def __init__(self, screen: pygame.surface.Surface, limit_w, limit_h, dificultad: str):
        self.__configs = open_configs()
        self.fosa = Agujero(self.__configs)
        self.player_sprite = Hero(50,self.__configs)
        self.enemies = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle(self.player_sprite)
        self.dificultad = dificultad
        self.__mapa_config = self.__configs.get("config_mundo")
        self.__dificulty_config = self.__configs.get(self.dificultad)
        self.__enemis_config = self.__dificulty_config.get("enemigos")
        self.__max_enemies = self.__enemis_config["cantidad_e"]
        self.__max_trampas = self.__enemis_config["cantidad_t"]
        self.__player_win = False
        self.__limit_w = limit_w
        self.__limit_h = limit_h
        self.__main_screen = screen
        self.frutas = pygame.sprite.Group()
        self.coras = pygame.sprite.Group()
        self.fondo = pygame.image.load(self.__mapa_config["fondo"]).convert_alpha()
        self.__is_hitting = False
        self.__is_inmortal = False
        self.perdiste = False
        self.__tiempo = 0
        self.trampas = pygame.sprite.Group()
        self.__spawn_trampas = True
        self.__spawn_trampas_moment = 1

        self.__all_enemies = []
        self.__all_trampas = []
        self.spawnear_enemigos(self.__max_enemies)
        self.spawnear_trampas(self.__max_trampas)

    def run(self, delta_ms):
        self.check_colide()
        self.fosa.update(self.__main_screen)
        self.frutas.update(self.__main_screen)
        self.trampas.update(self.__main_screen)
        self.coras.update(self.__main_screen)
        self.enemies.update(delta_ms, self.__main_screen)
        self.player_sprite.update(delta_ms, self.__main_screen)

    def cargar_nuevas_configs(self, dificultad):
        self.dificultad = dificultad
        self.__configs = open_configs()
        self.__mapa_config = self.__configs.get("config_mundo")
        self.__dificulty_config = self.__configs.get(self.dificultad)
        self.__enemis_config = self.__dificulty_config.get("enemigos")
        self.__max_enemies = self.__enemis_config["cantidad_e"]
        self.__max_trampas = self.__enemis_config["cantidad_t"]

    def spawnear_enemigos(self, cantidad):
        for _ in range(cantidad):
            zambie = Zambie(100,self.player_sprite.rect, self.__enemis_config)
            fantom = Fantasma(100,self.player_sprite.rect, self.__enemis_config)

            self.__all_enemies.append(fantom)
            self.__all_enemies.append(zambie)

    def spawnear_trampas(self, cantidad_trampas):
        for _ in range(cantidad_trampas):
            spawn_moment = pygame.time.get_ticks()//1000
            trampa = Trampa(self.player_sprite.rect, self.__mapa_config, spawn_moment)
            self.__all_trampas.append(trampa)

    def create_enemigos(self, cantidad):
        for _ in range(cantidad):
            eleccion = random.randint(1,2)
            if eleccion == 1:
                zambie = Zambie(100,self.player_sprite.rect, self.__enemis_config)
                self.enemies.add(zambie)
            else:
                fantom = Fantasma(100,self.player_sprite.rect, self.__enemis_config)
                self.enemies.add(fantom)

    def create_trampas(self, cantidad_trampas):
        for _ in range(cantidad_trampas):
            spawn_moment = pygame.time.get_ticks()//1000
            trampa = Trampa(self.player_sprite.rect, self.__mapa_config, spawn_moment)
            self.trampas.add(trampa)
            trampa.spawn_trap = False

    def check_colide(self):
        if pygame.sprite.spritecollideany(self.player_sprite, self.enemies):
            self.__is_hitting = True
            #self.chek_hero_life(100)
            self.inmortal()
        else:
            self.__is_hitting = False
            self.inmortal()

        for fruta in self.frutas:
            if pygame.sprite.collide_rect(fruta, self.player_sprite):
                fruta.kill()
                self.player_sprite.puntaje += 10
                self.player_sprite.exp += 10

        for cora in self.coras:
            if pygame.sprite.collide_rect(cora, self.player_sprite):
                cora.kill()
                if self.player_sprite.vida == 500:
                    self.player_sprite.puntaje += 140
                else:
                    self.player_sprite.vida += 100

        for trampa in self.trampas:
            if pygame.sprite.collide_rect(trampa, self.player_sprite):
                trampa.kill()
                self.chek_hero_life(200)

        
        cantidad_antes = len(self.enemies)
        for bullet in self.player_sprite.get_bullets:
            for enemi in self.enemies:
                if pygame.sprite.collide_rect(bullet, enemi):
                    bullet.kill()
                    enemi.vida -= self.player_sprite.daño_bala
                    self.check_enemi_death()
            
        for flecha in self.player_sprite.get_flechas:
            for enemi in self.enemies:
                if pygame.sprite.collide_rect(flecha, enemi):
                    enemi.vida -= self.player_sprite.daño_flecha
                    self.check_enemi_death()
        cantidad_despues = len(self.enemies)


        if self.fosa.get_rect().colliderect(self.player_sprite.rect_arr_collition):
            self.player_sprite.rect.top = self.fosa.get_rect().bottom + 5
        
        if self.fosa.get_rect().colliderect(self.player_sprite.rect_abj_collition):
            self.player_sprite.rect.bottom = self.fosa.get_rect().top - 5
        
        if self.fosa.get_rect().colliderect(self.player_sprite.rect_der_collition):
            self.player_sprite.rect.right = self.fosa.get_rect().left - 5
        
        if self.fosa.get_rect().colliderect(self.player_sprite.rect_izq_collition):
            self.player_sprite.rect.left = self.fosa.get_rect().right + 5
        
        

        if cantidad_antes > cantidad_despues:
            cantidad_vencido = cantidad_antes - cantidad_despues
            self.player_sprite.puntaje += cantidad_vencido * 50
            print(f'Puntaje actual: {self.player_sprite.puntaje} Puntos')


        if len(self.enemies) < len(self.__all_enemies):
            cantidad_e = len(self.__all_enemies) - len(self.enemies)
            self.create_enemigos(cantidad_e)

        if len(self.trampas) < len(self.__all_trampas):
            cantidad_t = len(self.__all_trampas) - len(self.trampas)
            self.create_trampas(cantidad_t)
                    

    def chek_hero_life(self, dano: int):
        if not self.__is_inmortal:
            self.player_sprite.vida -= dano
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
                rand = random.randint(1,23)
                if rand <= 21:
                    self.frutas.add(Fruta(self.__configs,pos_x,pos_y, "gema"))
                else:
                    self.coras.add(Fruta(self.__configs,pos_x,pos_y, "heart"))
                enemi.kill()

    