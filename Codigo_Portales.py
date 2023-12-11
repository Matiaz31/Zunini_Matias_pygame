import pygame
from Codigo_Assets import (ALTO_VENTANA, ANCHO_VENTANA, DEBUG)

class Portales():
    def __init__(self, diccionario,coord_x,coord_y):
        self.__mundo_config = diccionario.get("config_mundo")
        self.__portal_on_img = pygame.image.load(self.__mundo_config["portal_on"])
        self.__portal_off_img = pygame.image.load(self.__mundo_config["portal_off"])

        self.__portal_cooldawn = 14
        self.portal_moment = 1
        self.on = True


        if self.on:
            self.rect = self.__portal_on_img.get_rect()
        else:
            self.rect = self.__portal_off_img.get_rect()


        self.rect.x = coord_x
        self.rect.y = coord_y
        
        self.colisionrect_x = self.rect.x + 40
        self.colisionrect_y = self.rect.y + 40
        self.colisionrect_w = self.rect.w - 80
        self.colisionrect_h = self.rect.h - 80
        self.colisionrect = pygame.Rect(self.colisionrect_x,self.colisionrect_y,self.colisionrect_w,self.colisionrect_h)



    def draw(self, screen: pygame.surface.Surface):
        if self.on:
            screen.blit(self.__portal_on_img, self.rect)
        else:
            screen.blit(self.__portal_off_img, self.rect)
        if DEBUG:
            pygame.draw.rect(screen, "red", self.colisionrect)

    def update(self, screen: pygame.surface.Surface):
        self.draw(screen)
        self.prepared()

    def tp_recharge(self):
        momento = pygame.time.get_ticks()/1000
        if not self.on:
            if momento - self.portal_moment >= self.__portal_cooldawn:
                return True
        return False
    
    def prepared(self):
        if self.tp_recharge():
            self.portal_moment = pygame.time.get_ticks()/1000
            self.on = True

    def colision(self, player_rect, cual):
        if self.on == True:
            rect_arr_collition = pygame.Rect(player_rect.x + 12, player_rect.y, player_rect.width -30 ,2)
            rect_der_collition = pygame.Rect(player_rect.right, player_rect.y + 20, 2,player_rect.height - 30)
            rect_abj_collition = pygame.Rect(player_rect.x + 20, player_rect.bottom, player_rect.width - 30,2)
            rect_izq_collition = pygame.Rect(player_rect.x, player_rect.y + 20, 2,player_rect.height - 30)

            match cual:
                case 2:
                    if self.colisionrect.colliderect(rect_arr_collition):
                        self.on = False
                        player_rect.top = ALTO_VENTANA -150
                        player_rect.left = 30
                    if self.colisionrect.colliderect(rect_abj_collition):
                        self.on = False
                        player_rect.top = ALTO_VENTANA -150
                        player_rect.left = 30
                    if self.colisionrect.colliderect(rect_der_collition):
                        self.on = False
                        player_rect.top = ALTO_VENTANA -150
                        player_rect.left = 30
                    if self.colisionrect.colliderect(rect_izq_collition):
                        self.on = False
                        player_rect.top = ALTO_VENTANA -150
                        player_rect.left = 30

                case 1:
                    if self.colisionrect.colliderect(rect_arr_collition):
                        self.on = False
                        player_rect.top = 30
                        player_rect.left = ANCHO_VENTANA-150
                    if self.colisionrect.colliderect(rect_abj_collition):
                        self.on = False
                        player_rect.top = 30
                        player_rect.left = ANCHO_VENTANA-150
                    if self.colisionrect.colliderect(rect_der_collition):
                        self.on = False
                        player_rect.top = 30
                        player_rect.left = ANCHO_VENTANA-150
                    if self.colisionrect.colliderect(rect_izq_collition):
                        self.on = False
                        player_rect.top = 30
                        player_rect.left = ANCHO_VENTANA-150