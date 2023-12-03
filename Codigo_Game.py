import pygame
import sys
from Codigo_Button import Button
from Codigo_Stage import Stage
from Codigo_Assets import ANCHO_VENTANA, ALTO_VENTANA
from Codigo_Auxi import get_font

pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
clock = pygame.time.Clock()

class Game:
    def __init__(self, stage_name: str) -> None:
        self.game = Stage(pantalla, ANCHO_VENTANA, ALTO_VENTANA, stage_name)
        pygame.init()

    def play(self):

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.options()

            pantalla.blit(self.game.fondo, (0,0))
            delta_ms = clock.tick(60)
            self.game.run(delta_ms)
            pygame.display.flip()

    def main_menu(self):
        menu = True
        while menu:
            pantalla.blit(self.game.fondo, (0, 0))

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
                        self.play()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.play()
                        menu = False
                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.options()
                        menu = False
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        sys.exit()

            pygame.display.update()

    def options(self):
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
                        self.play()
                    if MEIN_MENU_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                        self.main_menu()

            pygame.display.update()