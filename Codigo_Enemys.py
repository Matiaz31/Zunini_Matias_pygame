import pygame
import random
from Codigo_Assets import (ALTO_VENTANA, ANCHO_VENTANA)
from Codigo_Auxi import SurfaceManager as sf

class Zambie(pygame.sprite.Sprite):
    def __init__(self,frame_rate, hero_rect, diccionario):
        super().__init__()
        self.__walk_r = sf.get_surface_from_spritesheet("Renders\zambie_walk.png", 6, 1)
        self.__walk_l = sf.get_surface_from_spritesheet("Renders\zambie_walk.png", 6, 1, flip=True)
        self.__atack_r = sf.get_surface_from_spritesheet("Renders\zambie_atack.png", 5, 1)
        self.__atack_l = sf.get_surface_from_spritesheet("Renders\zambie_atack.png", 5, 1, flip=True)
        self.__muerte_r = sf.get_surface_from_spritesheet("Renders\zambie_death.png", 5, 1)
        self.__muerte_l = sf.get_surface_from_spritesheet("Renders\zambie_death.png", 5, 1, flip=True)

        self.enemigos = []

        self.__move_x = 0
        self.__move_y = 0

        self.__speed_walk = random.randint(4,7)
        self.__frame_rate = frame_rate
        self.__actual_animation = self.__walk_r

        self.__enemy_move_time = 0
        self.__enemy_animation_time = 0
        self.__actual_frame = 0

        self.__actual_img_animation = self.__actual_animation[self.__actual_frame]
        self.__rect = self.__actual_img_animation.get_rect()
        self.__is_looking_right = True

        self.__rect.x = random.randint(0,1080)
        self.__rect.y = random.randint(0,200)
        self.sprite_group = pygame.sprite.Group()

        self.__hero_rect = hero_rect
        self.__is_atacking = False

        self.__is_alive = True
        self.__spawn_momento = 0
        

    def __set_x_animations_preset(self, move_x, animation_list: list[pygame.surface.Surface], look_r: bool):
        self.__move_x = move_x
        self.__is_looking_right = look_r
        if self.__actual_animation != animation_list:
            self.__actual_frame = 0
            self.__actual_animation = animation_list
    
    def __set_y_animations_preset(self, move_y, animation_list: list[pygame.surface.Surface], look_r: bool):
        self.__move_y = move_y
        if self.__actual_animation != animation_list:
            self.__actual_frame = 0
            self.__actual_animation = animation_list

    def walk(self):
        print(self.__hero_rect)
        if self.__rect.centerx < self.__hero_rect.centerx:
            look_right = True
            self.__set_x_animations_preset(self.__speed_walk, self.__walk_r, look_right)
        else:
            look_right = False
            self.__set_x_animations_preset(-self.__speed_walk, self.__walk_l, look_right)
        if self.__rect.centery < self.__hero_rect.centery:
            look_right = self.__is_looking_right
            if look_right == True:
                self.__set_y_animations_preset(self.__speed_walk, self.__walk_r,look_right)
            else:
                self.__set_y_animations_preset(self.__speed_walk, self.__walk_l,look_right)
        else:
            look_right = self.__is_looking_right
            if look_right == True:
                self.__set_y_animations_preset(-self.__speed_walk, self.__walk_r,look_right)
            else:
                self.__set_y_animations_preset(-self.__speed_walk, self.__walk_l,look_right)


    def atack(self):
        look_right = self.__is_looking_right
        rango_y = self.__hero_rect.centery - self.__rect.centery
        if self.__is_looking_right:
            rango_x = self.__hero_rect.centerx - self.__rect.centerx
            if rango_x <= 40 and rango_y <= 55 and rango_y >= -50:
                self.__set_x_animations_preset(0, self.__atack_r,look_right)
                self.__is_atacking = True
              
        else:
            rango_x = self.__hero_rect.centerx - self.__rect.centerx
            if rango_x >= -40 and rango_y <= 55 and rango_y >= -50: 
                self.__set_x_animations_preset(0, self.__atack_l,look_right)
                self.__is_atacking = True
             

        self.__is_atacking = False


    def draw(self, screen: pygame.surface.Surface):
        self.__actual_img_animation = self.__actual_animation[self.__actual_frame]
        screen.blit(self.__actual_img_animation, self.__rect)

    def __set_borders_limits_x(self):
        pixels_move = 0
        if self.__move_x > 0:
            pixels_move = self.__move_x if self.__rect.x < ANCHO_VENTANA - self.__actual_img_animation.get_width() else 0
        elif self.__move_x < 0:
            pixels_move = self.__move_x if self.__rect.x > 0 else 0
        return pixels_move
    
    def __set_borders_limits_y(self):
        pixels_move = 0
        if self.__move_y > 0:
            pixels_move = self.__move_y if self.__rect.y < ALTO_VENTANA - self.__actual_img_animation.get_height() else 0
        elif self.__move_y < 0:
            pixels_move = self.__move_y if self.__rect.y > 0 else 0
        return pixels_move
    

    def do_movement(self, delta_ms):
        self.__enemy_move_time += delta_ms
        if self.__enemy_move_time >= self.__frame_rate:
            self.__enemy_move_time = 0
            self.__rect.x += self.__set_borders_limits_x()
            self.__rect.y += self.__set_borders_limits_y()

    def do_animation(self, delta_ms):
        self.__enemy_animation_time += delta_ms
        if self.__enemy_animation_time >= self.__frame_rate:
            self.__enemy_animation_time = 0
            if self.__actual_frame < len(self.__actual_animation) - 1:
                self.__actual_frame += 1
            else:
                self.__actual_frame = 0
    
    def update(self, delta_ms, screen: pygame.surface.Surface):
        self.walk()
        self.atack()
        self.do_movement(delta_ms)
        self.do_animation(delta_ms)
        self.sprite_group.update()
        self.draw(screen)

    def draw(self, screen: pygame.surface.Surface):
        self.__actual_img_animation = self.__actual_animation[self.__actual_frame]
        screen.blit(self.__actual_img_animation, self.__rect)

    def generador(self):
        momento = pygame.time.get_ticks()/1000
        if momento - self.__spawn_momento >= 2:
            enemigo = self(self.__frame_rate, self.__hero_rect)
            pygame.sprite.Group.add(enemigo)
            self.__spawn_momento = pygame.time.get_ticks()/1000



class Fantasma(pygame.sprite.Sprite):
    def __init__(self,frame_rate):
        super().__init__()
        self.__walk_l = sf.get_surface_from_spritesheet(r"Renders\fantasma_walk.png", 12, 1)
        self.__walk_r = sf.get_surface_from_spritesheet(r"Renders\fantasma_walk.png", 12, 1, flip=True)
        self.__muerte_r = sf.get_surface_from_spritesheet(r"Renders\fantasma_muerte.png", 5, 1)
        self.__muerte_l = sf.get_surface_from_spritesheet(r"Renders\fantasma_muerte.png", 5, 1, flip=True)
        self.__move_x = 0
        self.__move_y = 0
        self.__speed_walk = random.randint(7,10)
        self.__frame_rate = frame_rate
        self.__actual_animation = self.__walk_r
        self.__enemy_move_time = 0
        self.__enemy_animation_time = 0
        self.__actual_frame = 0
        self.__actual_img_animation = self.__actual_animation[self.__actual_frame]
        self.__rect = self.__actual_img_animation.get_rect()
        self.__is_looking_right = True
        self.__rect.x = random.randint(0,200)
        self.__rect.y = random.randint(0,600)
        self.sprite_group = pygame.sprite.Group()


    def __set_borders_limits_x(self):
        pixels_move = 0
        if self.__move_x > 0:
            if self.__rect.x < ANCHO_VENTANA - self.__actual_img_animation.get_width():
                pixels_move = self.__move_x
            else:

                0
        elif self.__move_x < 0:
            pixels_move = self.__move_x if self.__rect.x > 0 else 0
        return pixels_move
    
    def __set_borders_limits_y(self):
        pixels_move = 0
        if self.__move_y > 0:
            pixels_move = self.__move_y if self.__rect.y < ALTO_VENTANA - self.__actual_img_animation.get_height() else 0
        elif self.__move_y < 0:
            pixels_move = self.__move_y if self.__rect.y > 0 else 0
        return pixels_move
    
    def do_animation(self, delta_ms):
        self.__enemy_animation_time += delta_ms
        if self.__enemy_animation_time >= self.__frame_rate:
            self.__enemy_animation_time = 0
            if self.__actual_frame < len(self.__actual_animation) - 1:
                self.__actual_frame += 1
            else:
                self.__actual_frame = 0

    def do_movement(self, delta_ms):
        self.__enemy_move_time += delta_ms
        if self.__enemy_move_time >= self.__frame_rate:
            self.__enemy_move_time = 0
            self.__rect.x += self.__set_borders_limits_x()
            self.__rect.y += self.__set_borders_limits_y()

    def __set_x_animations_preset(self, move_x, animation_list: list[pygame.surface.Surface], look_r: bool):
        self.__move_x = move_x
        self.__actual_animation = animation_list
        self.__is_looking_right = look_r

    def __set_y_animations_preset(self, move_y, animation_list: list[pygame.surface.Surface], look_r: bool):
        self.__move_y = move_y
        self.__actual_animation = animation_list

    def walk(self):
        direccion = self.__is_looking_right
        match direccion:
            case True:
                self.__set_x_animations_preset(self.__speed_walk, self.__walk_r, direccion)
                if self.__rect.centerx >= ANCHO_VENTANA - 50:
                    self.__is_looking_right = False
            case _:
                    self.__set_x_animations_preset(-self.__speed_walk, self.__walk_l, direccion)
                    if self.__rect.centerx <= 50:
                        self.__is_looking_right = True


    def draw(self, screen: pygame.surface.Surface):
        self.__actual_img_animation = self.__actual_animation[self.__actual_frame]
        screen.blit(self.__actual_img_animation, self.__rect)

    def update(self, delta_ms, screen: pygame.surface.Surface):
        self.do_movement(delta_ms)
        self.do_animation(delta_ms)
        self.sprite_group.update()
        self.walk()
        self.draw(screen)
