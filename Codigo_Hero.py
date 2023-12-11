import pygame
from Codigo_Assets import (ALTO_VENTANA, ANCHO_VENTANA, DEBUG)
from Codigo_Bullet import Bala,Flecha
from Codigo_Auxi import SurfaceManager as sf

class Hero(pygame.sprite.Sprite):
    def __init__(self,frame_rate, diccionario):
        super().__init__()
        self.__player_config = diccionario.get("estadisticas_hero")
        self.__sprites_config = self.__player_config.get("sprites")

        self.vida = self.__player_config["vida"]

        self.daño_bala = 100
        self.daño_flecha = 7
        self.puntaje = 0
        self.exp = 0
        self.nivel = 1

        self.__iddle_l = sf.get_surface_from_spritesheet(self.__sprites_config["idle"], 3, 1, flip=True)
        self.__iddle_r = sf.get_surface_from_spritesheet(self.__sprites_config["idle"], 3, 1)
        self.__walk_l = sf.get_surface_from_spritesheet(self.__sprites_config["walk"], 6, 1, flip=True)
        self.__walk_r = sf.get_surface_from_spritesheet(self.__sprites_config["walk"], 6, 1)
        self.__is_stay = True

        self.__bullet_img = self.__sprites_config["bala"]
        self.__flecha_img_r = self.__sprites_config["flecha_r"]
        self.__flecha_img_l = self.__sprites_config["flecha_l"]

        self.__move_x = 0
        self.__move_y = 0
        self.speed_walk = self.__player_config["velocidad"]
        self.__frame_rate = frame_rate

        self.__player_move_time = 0
        self.__player_animation_time = 0
        self.__initial_frame = 0
        self.__actual_animation = self.__iddle_r
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        self.__is_looking_right = True

        self.rect = self.__actual_img_animation.get_rect()
        self.rect.x = ANCHO_VENTANA/2
        self.rect.y = ALTO_VENTANA/2
        self.is_coliding = False

        self.rect_arr_collition = pygame.Rect(self.rect.x + 12, self.rect.y, self.rect.width -30 ,2)
        self.rect_der_collition = pygame.Rect(self.rect.right, self.rect.y - 20, 2,self.rect.height - 30)
        self.rect_abj_collition = pygame.Rect(self.rect.x + 20, self.rect.bottom, self.rect.width - 30,2)
        self.rect_izq_collition = pygame.Rect(self.rect.x, self.rect.y - 20, 2,self.rect.height - 30)
        
        self.__bala_cooldawn = self.__player_config["cooldawn_bala"]
        self.__flecha_cooldawn = self.__player_config["cooldawn_flecha"]

        self.__bullet_moment = 1
        self.__fire_bullet = False
        self.__flecha_moment = 1
        self.__fire_flecha = False

        self.__sprite_bullet_group = pygame.sprite.Group()
        self.__sprite_flecha_group = pygame.sprite.Group()

    @property
    def get_bullets(self) -> list[Bala]:
        return self.__sprite_bullet_group
    
    @property
    def get_flechas(self) -> list[Flecha]:
        return self.__sprite_flecha_group
    
    def __set_x_animations_preset(self, move_x, animation_list: list[pygame.surface.Surface], look_r: bool):
        self.__move_x = move_x
        self.__is_looking_right = look_r
        if self.__actual_animation != animation_list:
            self.__actual_frame = 0
            self.__actual_animation = animation_list
        
    def __set_y_animations_preset(self, move_y, animation_list: list[pygame.surface.Surface]):
        self.__move_y = move_y
        self.__actual_animation = animation_list
    
    def walk(self, direction: str = ""):
        self.__dash_direccion = direction
        self.__is_stay = False
        match direction:
            case "Right":
                look_right = True
                self.__set_x_animations_preset(self.speed_walk, self.__walk_r, look_right)

            case "Left":
                look_right = False
                self.__set_x_animations_preset(-self.speed_walk, self.__walk_l, look_right)

            case "Up":
                look_right = self.__is_looking_right
                if look_right:
                    self.__set_y_animations_preset(self.speed_walk, self.__walk_r)
                else:
                    self.__set_y_animations_preset(self.speed_walk, self.__walk_l)

            case "Down":
                look_right = self.__is_looking_right
                if look_right:
                    self.__set_y_animations_preset(-self.speed_walk, self.__walk_r)
                else:
                    self.__set_y_animations_preset(-self.speed_walk, self.__walk_l)
        self.__is_stay = True

    def stay(self):
        if self.__is_stay:
            if self.__actual_animation != self.__iddle_l and self.__actual_animation != self.__iddle_r:
                self.__actual_animation = self.__iddle_r if self.__is_looking_right else self.__iddle_l
                self.__initial_frame = 0
                self.__move_x = 0
                self.__move_y = 0
    
    
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
        self.__player_move_time += delta_ms
        if self.__player_move_time >= self.__frame_rate:
            self.__player_move_time = 0
            self.rect.x += self.__set_borders_limits_x()
            self.rect.y += self.__set_borders_limits_y()
    
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
        self.boxes()
        self.stay()
        self.teclas()
        self.shoot(screen)
        self.do_movement(delta_ms)
        self.do_animation(delta_ms)
        self.__sprite_bullet_group.update()
        self.__sprite_bullet_group.draw(screen)
        self.__sprite_flecha_group.update()
        self.__sprite_flecha_group.draw(screen)
        self.draw(screen)
    
    def draw(self, screen: pygame.surface.Surface):
        if DEBUG:
            pygame.draw.rect(screen, "red", self.rect_abj_collition)
            pygame.draw.rect(screen, "red", self.rect_arr_collition)
            pygame.draw.rect(screen, "red", self.rect_der_collition)
            pygame.draw.rect(screen, "red", self.rect_izq_collition)
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        screen.blit(self.__actual_img_animation, self.rect)

    def shoot(self,pantalla):
        if self.shoot_recharge_bala():
            self.__bullet_moment = pygame.time.get_ticks()/1000
            for i in range(1,5):
                self.__sprite_bullet_group.add(self.bala_create(i))

        if self.shoot_recharge_flecha():
            self.__flecha_moment = pygame.time.get_ticks()/1000
            if self.__is_looking_right:
                self.__sprite_flecha_group.add(self.flecha_create("Right"))
            else:
                self.__sprite_flecha_group.add(self.flecha_create("Left"))
            self.__fire_bullet = False

    def shoot_recharge_bala(self):
        momento = pygame.time.get_ticks()/1000
        if not self.__fire_bullet:
            if momento - self.__bullet_moment >= self.__bala_cooldawn:
                return True
        return False
            
    def shoot_recharge_flecha(self):
        momento = pygame.time.get_ticks()/1000
        if not self.__fire_flecha:
            if momento - self.__flecha_moment >= self.__flecha_cooldawn:
                return True
        return False

    def bala_create(self, bala: int):
        if bala == 1:
            return Bala(self.rect.centerx,self.rect.centery,  self.__bullet_img, "Right-Up")
        elif bala == 2:
            return Bala(self.rect.centerx,self.rect.centery,  self.__bullet_img, "Left-Up")
        elif bala == 3:
            return Bala(self.rect.centerx,self.rect.centery,  self.__bullet_img, "Right-Down")
        elif bala == 4:
            return Bala(self.rect.centerx,self.rect.centery,  self.__bullet_img, "Left-Down")   
        
    def flecha_create(self, direccion: str):
        if direccion == "Right":
            return Flecha(self.rect.centerx,self.rect.centery,  self.__flecha_img_r, direccion)
        else:
            return Flecha(self.rect.centerx,self.rect.centery,  self.__flecha_img_l, direccion)

    def level_up(self):
        if self.nivel < 3:
            if self.exp >= 100:
                self.nivel += 1
                self.exp = 0
                return True
        elif self.nivel < 6:
            if self.exp >= 150:
                self.nivel += 1
                self.exp = 0
                return True
        elif self.nivel > 6:
            if self.exp >= 150:
                self.nivel += 1
                self.exp = 0
                return True
        return False

    def boxes(self):
        self.rect_arr_collition = pygame.Rect(self.rect.x + 12, self.rect.y, self.rect.width -30 ,2)
        self.rect_der_collition = pygame.Rect(self.rect.right, self.rect.y + 20, 2,self.rect.height - 30)
        self.rect_abj_collition = pygame.Rect(self.rect.x + 20, self.rect.bottom, self.rect.width - 30,2)
        self.rect_izq_collition = pygame.Rect(self.rect.x, self.rect.y + 20, 2,self.rect.height - 30)
    
    # def dash(self):
    #     if self.dash_recharge():
    #         self.__dash_moment = pygame.time.get_ticks()/1000
    #         match self.__dash_direccion:
    #             case "Right":
    #                 look_right = True
    #                 self.__set_x_animations_preset(self.__dash_power, self.__walk_r, look_right)
    #             case "Left":
    #                 look_right = False
    #                 self.__set_x_animations_preset(-self.__dash_power, self.__walk_r, look_right)
    #         self.__dash = False
                
    # def dash_recharge(self):
    #     momento = pygame.time.get_ticks()/1000
    #     if not self.__dash:
    #         if momento - self.__dash_moment <= self.__dash_cooldawn:
    #             return True
    #     return False
