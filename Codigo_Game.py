import pygame
import sys
from Codigo_Button import Button
from Codigo_Stage import Stage
from Codigo_Assets import ANCHO_VENTANA, ALTO_VENTANA
from Codigo_Auxi import get_font

pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
clock = pygame.time.Clock()
icon = pygame.image.load('Renders/gema.png')
class Game:
    def __init__(self, stage_name: str) -> None:
        self.dificultad = stage_name
        self.game = Stage(pantalla, ANCHO_VENTANA, ALTO_VENTANA, self.dificultad)
        pygame.init()
        pygame.display.set_caption("Wizzzard")
        pygame.display.set_icon(icon)
        self.volumen = 0
        self.tiempo_transcurrido = 0
        
    def play(self):
        print(self.dificultad)
        self.game.play_music(self.volumen, "Renders\Arabesque.mp3")
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.options()
            if self.game.perdiste == True:
                self.you_lost()
            
            delta_ms = clock.tick(60)
            pantalla.blit(self.game.fondo, (0,0))
            self.tiempo_transcurrido = pygame.time.get_ticks()//1000
            pantalla.blit(get_font(40).render(f"Tiempo: {self.tiempo_transcurrido}",True, "Black"), (10,10))
            self.game.run(delta_ms)
            #self.game.enemies_hit()
            pygame.display.update()
            if self.tiempo_transcurrido > 59 and self.tiempo_transcurrido < 120:
                self.dificultad = "dificultad_2"
                print(self.dificultad)
            elif self.tiempo_transcurrido > 120:
                self.dificultad = "dificultad_3"
                print(self.dificultad)

    def main_menu(self):
        self.game.play_music(self.volumen, "Renders\menu_chill.wav")
        menu = True
        while menu:
            pantalla.blit(self.game.fondo, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
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

            pantalla.fill((150,190,190))

            OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
            OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(ANCHO_VENTANA/2, 260))
            pantalla.blit(OPTIONS_TEXT, OPTIONS_RECT)
            VOLUMEN_TXT = get_font(75).render(f"Volumen: {round(self.volumen,1)}", True, "Black")
            pantalla.blit(VOLUMEN_TXT,(380,430))

            OPTIONS_BACK = Button(image=None, pos=(ANCHO_VENTANA/2, 350), 
                                text_input="Play", font=get_font(75), base_color="Black", hovering_color=(20,120,0))
            MEIN_MENU_BUTTON = Button(image=None, pos=(ANCHO_VENTANA/2, 400), 
                                text_input="Menu", font=get_font(75), base_color="Black", hovering_color=(20,120,0))
            VOLUME_MAS = Button(image=None, pos=(ANCHO_VENTANA/1.5, 450), 
                                text_input="+", font=get_font(75), base_color="Black", hovering_color=(20,120,0))
            VOLUME_MENOS = Button(image=None, pos=(360, 450), 
                                text_input="-", font=get_font(75), base_color="Black", hovering_color=(20,120,0))

            OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
            OPTIONS_BACK.update(pantalla)
            MEIN_MENU_BUTTON.changeColor(OPTIONS_MOUSE_POS)
            MEIN_MENU_BUTTON.update(pantalla)
            VOLUME_MAS.changeColor(OPTIONS_MOUSE_POS)
            VOLUME_MAS.update(pantalla)
            VOLUME_MENOS.changeColor(OPTIONS_MOUSE_POS)
            VOLUME_MENOS.update(pantalla)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                        self.play()
                    if MEIN_MENU_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                        self.main_menu()
                    if VOLUME_MAS.checkForInput(OPTIONS_MOUSE_POS):
                        if self.volumen < 0.9:
                            self.volumen += 0.1
                    if VOLUME_MENOS.checkForInput(OPTIONS_MOUSE_POS):
                        if self.volumen > 0.1:
                            self.volumen -= 0.1

            pygame.display.update()
    
    def you_lost(self):
        if self.game.perdiste==True:
            while True:
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()

                pantalla.blit(self.game.fondo,(0,0))
                Texto = get_font(150).render("Game Over",True, "Black")
                pantalla.blit(Texto,(260,170))

                pygame.display.update()