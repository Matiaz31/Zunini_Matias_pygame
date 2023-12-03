import pygame
from Codigo_Assets import (ALTO_VENTANA, ANCHO_VENTANA, FPS)
from Codigo_Button import Button
from Codigo_Hero import Hero
from Codigo_Enemys import Zambie,Fantasma
from Codigo_Auxi import get_font

pygame.init()

pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))

fondo = pygame.image.load(r'Renders\fondo.png').convert_alpha()
pygame.display.set_caption("Wizzzard")

clock = pygame.time.Clock()

magito = Hero(50, 8)

sprites_enemis = pygame.sprite.Group()
sprites_magito = pygame.sprite.GroupSingle(magito)

for _ in range(10):
    zambie = Zambie(100,magito.get_rect)
    fantom = Fantasma(100)
    zambie.enemigos.append(zambie)
    sprites_enemis.add(fantom)
    sprites_enemis.add(zambie)

lista_eventos = pygame.event.get()

def play():
    playing : True
    while True:
        pantalla.blit(fondo, (0, 0))

        delta_ms = clock.tick(FPS)
        magito.stay()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    options()
                    
                if event.key == pygame.K_SPACE:
                    print("DASHED")
                    magito.dash()
  
        # lista_teclas_presionadas = pygame.key.get_pressed()
        # if lista_teclas_presionadas[pygame.K_RIGHT] and not lista_teclas_presionadas[pygame.K_LEFT]:
        #     magito.walk('Right')
        # if lista_teclas_presionadas[pygame.K_LEFT] and not lista_teclas_presionadas[pygame.K_RIGHT]:
        #     magito.walk('Left')
        # if lista_teclas_presionadas[pygame.K_UP] and not lista_teclas_presionadas[pygame.K_DOWN]:
        #     magito.walk('Down')
        # if lista_teclas_presionadas[pygame.K_DOWN] and not lista_teclas_presionadas[pygame.K_UP]:
        #     magito.walk('Up')


        #sprites_enemis.draw(pantalla)
        sprites_enemis.update(delta_ms, pantalla)

        magito.update(delta_ms, pantalla)
        magito.shoot(pantalla)
        magito.sprite_group.draw(pantalla)

        pygame.display.update()

def options():
    playing : False
    print("opcions")
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        pantalla.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(ANCHO_VENTANA/2, 260))
        pantalla.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(ANCHO_VENTANA/2, 400), 
                            text_input="Play", font=get_font(75), base_color="Black", hovering_color="Green")
        MEIN_MENU_BUTTON = Button(image=None, pos=(ANCHO_VENTANA/2, 460), 
                            text_input="Menu", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(pantalla)
        MEIN_MENU_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        MEIN_MENU_BUTTON.update(pantalla)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    play()
                if MEIN_MENU_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    menu = True
    while menu:
        pantalla.blit(fondo, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(75).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(ANCHO_VENTANA/2, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("Renders\Play Rect.png"), pos=(ANCHO_VENTANA/2, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("Renders\Options Rect.png"), pos=(ANCHO_VENTANA/2, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("Renders\Quit Rect.png"), pos=(ANCHO_VENTANA/2, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        pantalla.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(pantalla)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    play()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                    menu = False
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                    menu = False
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()

        pygame.display.update()

main_menu()
