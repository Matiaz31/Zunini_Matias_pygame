import pygame
import random
from Codigo_Assets import (ALTO_VENTANA, ANCHO_VENTANA)
from Codigo_Auxi import SurfaceManager as sf

class Zambie(pygame.sprite.Sprite):
    def __init__(self,frame_rate, hero_rect, diccionario):
        super().__init__()
        self.__config = diccionario.get("zombie")
        self.__sprite_config = self.__config.get("sprites")

        self.__walk_r = sf.get_surface_from_spritesheet(self.__sprite_config["walk"], 6, 1)
        self.__walk_l = sf.get_surface_from_spritesheet(self.__sprite_config["walk"], 6, 1, flip=True)
        self.__atack_r = sf.get_surface_from_spritesheet(self.__sprite_config["atack"], 5, 1)
        self.__atack_l = sf.get_surface_from_spritesheet(self.__sprite_config["atack"], 5, 1, flip=True)
        self.__muerte_r = sf.get_surface_from_spritesheet(self.__sprite_config["muerte"], 5, 1)
        self.__muerte_l = sf.get_surface_from_spritesheet(self.__sprite_config["muerte"], 5, 1, flip=True)

        self.__move_x = 0
        self.__move_y = 0

        self.__speed_walk = random.randint(4,7)
        self.__frame_rate = frame_rate
        self.__actual_animation = self.__walk_r

        self.__enemy_move_time = 0
        self.__enemy_animation_time = 0
        self.__actual_frame = 0

        self.__actual_img_animation = self.__actual_animation[self.__actual_frame]
        self.rect = self.__actual_img_animation.get_rect()
        self.__is_looking_right = True

        self.__hero_rect = hero_rect
        self.__hero_x_1 = self.__hero_rect.centerx - 100
        self.__hero_y_1 = self.__hero_rect.centery - 100
        self.__hero_x_2 = self.__hero_rect.centerx + 100
        self.__hero_y_2 = self.__hero_rect.centery + 100

        self.x = random.randint(0,ANCHO_VENTANA)
        if self.x > self.__hero_x_1 and self.x < self.__hero_x_2:
            pass
        else:
            self.rect.x = self.x
        self.y = random.randint(0,ALTO_VENTANA)
        if self.y > self.__hero_y_1 and self.y < self.__hero_y_2:
            pass
        else:
            self.rect.y = self.y

        self.sprite_group = pygame.sprite.Group()
        self.__is_atacking = False
        self.__is_alive = True
        self.vida = self.__config["vida"]

        

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
        if self.rect.centerx < self.__hero_rect.centerx:
            look_right = True
            self.__set_x_animations_preset(self.__speed_walk, self.__walk_r, look_right)
        else:
            look_right = False
            self.__set_x_animations_preset(-self.__speed_walk, self.__walk_l, look_right)
        if self.rect.centery < self.__hero_rect.centery:
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
        rango_y = self.__hero_rect.centery - self.rect.centery
        if self.__is_looking_right:
            rango_x = self.__hero_rect.centerx - self.rect.centerx
            if rango_x <= 40 and rango_y <= 55 and rango_y >= -50:
                self.__set_x_animations_preset(0, self.__atack_r,look_right)
                self.__is_atacking = True
              
        else:
            rango_x = self.__hero_rect.centerx - self.rect.centerx
            if rango_x >= -40 and rango_y <= 55 and rango_y >= -50: 
                self.__set_x_animations_preset(0, self.__atack_l,look_right)
                self.__is_atacking = True
             

        self.__is_atacking = False


    def draw(self, screen: pygame.surface.Surface):
        self.__actual_img_animation = self.__actual_animation[self.__actual_frame]
        screen.blit(self.__actual_img_animation, self.rect)

    def __set_borders_limits_x(self):
        pixels_move = 0
        if self.__move_x > 0:
            pixels_move = self.__move_x if self.rect.x < ANCHO_VENTANA - self.__actual_img_animation.get_width() else 0
        elif self.__move_x < 0:
            pixels_move = self.__move_x if self.rect.x > 0 else 0
        return pixels_move
    
    def __set_borders_limits_y(self):
        pixels_move = 0
        if self.__move_y > 0:
            pixels_move = self.__move_y if self.rect.y < ALTO_VENTANA - self.__actual_img_animation.get_height() else 0
        elif self.__move_y < 0:
            pixels_move = self.__move_y if self.rect.y > 0 else 0
        return pixels_move
    

    def do_movement(self, delta_ms):
        self.__enemy_move_time += delta_ms
        if self.__enemy_move_time >= self.__frame_rate:
            self.__enemy_move_time = 0
            self.rect.x += self.__set_borders_limits_x()
            self.rect.y += self.__set_borders_limits_y()

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
        screen.blit(self.__actual_img_animation, self.rect)



class Fantasma(pygame.sprite.Sprite):
    def __init__(self,frame_rate, hero_rect, diccionario):
        super().__init__()
        self.__config = diccionario.get("fantom")
        self.__sprite_config = self.__config.get("sprites")

        self.__walk_l = sf.get_surface_from_spritesheet(self.__sprite_config["walk"], 12, 1)
        self.__walk_r = sf.get_surface_from_spritesheet(self.__sprite_config["walk"], 12, 1, flip=True)
        self.__muerte_r = sf.get_surface_from_spritesheet(self.__sprite_config["muerte"], 5, 1)
        self.__muerte_l = sf.get_surface_from_spritesheet(self.__sprite_config["muerte"], 5, 1, flip=True)

        self.__move_x = 0
        self.__move_y = 0
        self.__speed_walk = random.randint(7,10)
        self.__frame_rate = frame_rate

        self.__actual_animation = self.__walk_r
        self.__enemy_move_time = 0
        self.__enemy_animation_time = 0
        self.__actual_frame = 0
        self.__actual_img_animation = self.__actual_animation[self.__actual_frame]
        self.__is_looking_right = True

        self.__hero_rect = hero_rect

        self.rect = self.__actual_img_animation.get_rect()
        self.x = random.randint(10,ANCHO_VENTANA)
        if self.x > self.__hero_rect.centerx - 100 and self.x < self.__hero_rect.centerx + 100:
            self.x = random.randint(0,ANCHO_VENTANA)
        else:
            self.rect.x = self.x

        self.y = random.randint(400,ALTO_VENTANA)
        if self.y > self.__hero_rect.centery - 100 and self.y < self.__hero_rect.centery + 100:
            self.y = random.randint(400,ALTO_VENTANA)
        else:
            self.rect.y = self.y

        self.sprite_group = pygame.sprite.Group()
        self.vida = self.__config["vida"]
        self.is_alive = True

    def __set_borders_limits_x(self):
        pixels_move = 0
        if self.__move_x > 0:
            if self.rect.x < ANCHO_VENTANA - self.__actual_img_animation.get_width():
                pixels_move = self.__move_x
            else:

                0
        elif self.__move_x < 0:
            pixels_move = self.__move_x if self.rect.x > 0 else 0
        return pixels_move
    
    def __set_borders_limits_y(self):
        pixels_move = 0
        if self.__move_y > 0:
            pixels_move = self.__move_y if self.rect.y < ALTO_VENTANA - self.__actual_img_animation.get_height() else 0
        elif self.__move_y < 0:
            pixels_move = self.__move_y if self.rect.y > 0 else 0
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
            self.rect.x += self.__set_borders_limits_x()
            self.rect.y += self.__set_borders_limits_y()

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
                if self.rect.centerx >= ANCHO_VENTANA - 50:
                    self.__is_looking_right = False
            case _:
                    self.__set_x_animations_preset(-self.__speed_walk, self.__walk_l, direccion)
                    if self.rect.centerx <= 50:
                        self.__is_looking_right = True


    def draw(self, screen: pygame.surface.Surface):
        self.__actual_img_animation = self.__actual_animation[self.__actual_frame]
        screen.blit(self.__actual_img_animation, self.rect)

    def update(self, delta_ms, screen: pygame.surface.Surface):
        self.do_movement(delta_ms)
        self.do_animation(delta_ms)
        self.sprite_group.update()
        self.walk()
        self.draw(screen)

class Trampa(pygame.sprite.Sprite):
    def __init__(self, hero_rect , diccionario, momento):
        super().__init__()
        self.__mundo_config = diccionario
        self.__trampa_img = pygame.transform.scale(pygame.image.load(self.__mundo_config["trampa"]),(35,35))

        self.rect = self.__trampa_img.get_rect()

        self.__hero_rect = hero_rect
        self.__hero_x_1 = self.__hero_rect.centerx - 100
        self.__hero_y_1 = self.__hero_rect.centery - 100
        self.__hero_x_2 = self.__hero_rect.centerx + 100
        self.__hero_y_2 = self.__hero_rect.centery + 100

        self.x = random.randint(0,ANCHO_VENTANA)
        if self.x > self.__hero_x_1 and self.x < self.__hero_x_2:
            pass
        else:
            self.rect.x = self.x
        self.y = random.randint(0,ALTO_VENTANA)
        if self.y > self.__hero_y_1 and self.y < self.__hero_y_2:
            pass
        else:
            self.rect.y = self.y

        self.__spawn_moment = momento
        self.spawn_trap = True
    
    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self.__trampa_img, self.rect)

    def update(self, screen: pygame.surface.Surface):
        self.recolocar_trampas()
        self.draw(screen)

    def recolocar_trampas(self):
        if self.recharge_traps():
            self.x = random.randint(0,ANCHO_VENTANA)
            if self.x > self.__hero_x_1 and self.x < self.__hero_x_2:
                pass
            else:
                self.rect.x = self.x

            self.y = random.randint(0,ALTO_VENTANA)
            if self.y > self.__hero_y_1 and self.y < self.__hero_y_2:
                pass
            else:
                self.rect.y = self.y
            self.__spawn_moment = pygame.time.get_ticks()//1000

    def recharge_traps(self):
        momento = pygame.time.get_ticks()//1000
        if not self.spawn_trap:
            if momento - self.__spawn_moment >= 5:
                return True
        return False