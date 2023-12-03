import pygame
from Codigo_Assets import (ALTO_VENTANA, ANCHO_VENTANA)
from Codigo_Bullet import Bullet
from Codigo_Auxi import SurfaceManager as sf
import random

class Hero(pygame.sprite.Sprite):
    def __init__(self,frame_rate, speed_walk):
        super().__init__()
        self.__iddle_l = sf.get_surface_from_spritesheet("Renders\hero_iddle.png", 3, 1, flip=True)
        self.__iddle_r = sf.get_surface_from_spritesheet("Renders\hero_iddle.png", 3, 1)
        self.__walk_l = sf.get_surface_from_spritesheet("Renders\hero_walk.png", 6, 1, flip=True)
        self.__walk_r = sf.get_surface_from_spritesheet("Renders\hero_walk.png", 6, 1)

        self.__move_x = 0
        self.__move_y = 0
        self.__speed_walk = speed_walk
        self.__frame_rate = frame_rate

        self.__player_move_time = 0
        self.__player_animation_time = 0
        self.__initial_frame = 0

        self.__actual_animation = self.__iddle_r
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        self.__rect = self.__actual_img_animation.get_rect()
        self.__is_looking_right = True

        self.__rect.x = ANCHO_VENTANA/2
        self.__rect.y = ALTO_VENTANA/2

        self.__fire_moment = 1
        self.__fire_cooldawn = 3
        self.__fire = False

        self.__dash_moment = 1
        self.__dash_cooldawn = 2
        self.__dash = True
        self.__dash_power = 15
        self.__dash_direccion = "Right"

        self.sprite_group = pygame.sprite.Group()
        
    @property
    def get_rect(self):
        return self.__rect
    
    @property
    def get_x(self):
        return self.__rect.x
    
    @property
    def get_y(self):
        return self.__rect.y
    
    def __set_x_animations_preset(self, move_x, animation_list: list[pygame.surface.Surface], look_r: bool):
        self.__move_x = move_x
        self.__actual_animation = animation_list
        self.__is_looking_right = look_r
        
    def __set_y_animations_preset(self, move_y, animation_list: list[pygame.surface.Surface]):
        self.__move_y = move_y
        self.__actual_animation = animation_list
    
    def walk(self, direction: str = ""):
        self.__dash_direccion = direction
        match direction:
            case "Right":
                look_right = True
                self.__set_x_animations_preset(self.__speed_walk, self.__walk_r, look_right)

            case "Left":
                look_right = False
                self.__set_x_animations_preset(-self.__speed_walk, self.__walk_l, look_right)

            case "Up":
                look_right = self.__is_looking_right
                if look_right:
                    self.__set_y_animations_preset(self.__speed_walk, self.__walk_r)
                else:
                    self.__set_y_animations_preset(self.__speed_walk, self.__walk_l)

            case "Down":
                look_right = self.__is_looking_right
                if look_right:
                    self.__set_y_animations_preset(-self.__speed_walk, self.__walk_r)
                else:
                    self.__set_y_animations_preset(-self.__speed_walk, self.__walk_l)

    
    def stay(self):
        if self.__actual_animation != self.__iddle_l and self.__actual_animation != self.__iddle_r:
            self.__actual_animation = self.__iddle_r if self.__is_looking_right else self.__iddle_l
            self.__initial_frame = 0
            self.__move_x = 0
            self.__move_y = 0
    
    
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
        self.__player_move_time += delta_ms
        if self.__player_move_time >= self.__frame_rate:
            self.__player_move_time = 0
            self.__rect.x += self.__set_borders_limits_x()
            self.__rect.y += self.__set_borders_limits_y()
    
    def teclas(self):
        lista_teclas_presionadas = pygame.key.get_pressed()
        if lista_teclas_presionadas[pygame.K_RIGHT] and not lista_teclas_presionadas[pygame.K_LEFT]:
            self.walk("Right")
        if lista_teclas_presionadas[pygame.K_LEFT] and not lista_teclas_presionadas[pygame.K_RIGHT]:
            self.walk("Left")
        if lista_teclas_presionadas[pygame.K_UP] and not lista_teclas_presionadas[pygame.K_DOWN]:
            self.walk("Down")
        if lista_teclas_presionadas[pygame.K_DOWN] and not lista_teclas_presionadas[pygame.K_UP]:
            self.walk("Up")

    def do_animation(self, delta_ms):
        self.__player_animation_time += delta_ms
        if self.__player_animation_time >= self.__frame_rate:
            self.__player_animation_time = 0
            if self.__initial_frame < len(self.__actual_animation) - 1:
                self.__initial_frame += 1
            else:
                self.__initial_frame = 0
    
    def update(self, delta_ms, screen: pygame.surface.Surface):
        self.teclas()
        self.do_movement(delta_ms)
        self.do_animation(delta_ms)
        self.sprite_group.update() 
        self.draw(screen)
    
    def draw(self, screen: pygame.surface.Surface):
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        screen.blit(self.__actual_img_animation, self.__rect)

    def shoot(self,pantalla):
        if self.shoot_recharge():
            self.__fire_moment = pygame.time.get_ticks()/1000
            for i in range(1,5):
                self.sprite_group.add(self.shoot_create(i))
            self.fire = False

    def shoot_recharge(self):
        momento = pygame.time.get_ticks()/1000
        if not self.__fire:
            print(self.__fire_moment)
            if momento - self.__fire_moment >= self.__fire_cooldawn:
                print(momento)
                return True
        return False

    def shoot_create(self, bala: int):
        if bala == 1:
            return Bullet(self.__rect.centerx,self.__rect.centery, "Right-Up")
        elif bala == 2:
            return Bullet(self.__rect.centerx,self.__rect.centery, "Left-Up")
        elif bala == 3:
            return Bullet(self.__rect.centerx,self.__rect.centery, "Right-Down")
        elif bala == 4:
            return Bullet(self.__rect.centerx,self.__rect.centery, "Left-Down")   
    
    def dash(self):
        if self.dash_recharge():
            self.__dash_moment = pygame.time.get_ticks()/1000
            match self.__dash_direccion:
                case "Right":
                    look_right = True
                    self.__set_x_animations_preset(self.__dash_power, self.__walk_r, look_right)
                case "Left":
                    look_right = False
                    self.__set_x_animations_preset(-self.__dash_power, self.__walk_r, look_right)
            self.__dash = False
                
    def dash_recharge(self):
        momento = pygame.time.get_ticks()/1000
        if not self.__dash:
            if momento - self.__dash_moment <= self.__dash_cooldawn:
                return True
        return False
