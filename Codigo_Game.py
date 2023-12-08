import pygame
import sys
from Codigo_Button import Button
from Codigo_Stage import Stage
from Codigo_Assets import ANCHO_VENTANA, ALTO_VENTANA
from Codigo_Auxi import get_font, play_music

pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
clock = pygame.time.Clock()
icon = pygame.image.load('Renders/gema.png')
fondo_menu = pygame.image.load("Renders/fondo.png")

class Game:
    def __init__(self, stage_name: str) -> None:
        self.dificultad = stage_name
        pygame.init()
        pygame.display.set_caption("Wizzzard")
        pygame.display.set_icon(icon)
        self.volumen = 0
        self.tiempo_transcurrido = 0
        self.opciones = False
        self.menu = False


    def main_menu(self):
        play_music(self.volumen, 0, "Renders\menu_chill.wav")
        self.menu = True
        while self.menu:
            pantalla.blit(fondo_menu, (0, 0))

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
                    sys.exit()
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
        self.opciones = True
        while self.opciones:
            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

            pantalla.fill((150,190,190))

            OPTIONS_TEXT = get_font(45).render("Estas en la Pantalla de opciones", True, "Black")
            OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(ANCHO_VENTANA/2, 160))
            pantalla.blit(OPTIONS_TEXT, OPTIONS_RECT)
            VOLUMEN_TXT = get_font(75).render(f"Volumen: {round(self.volumen,1)}", True, "Black")
            pantalla.blit(VOLUMEN_TXT,(380,330))

            OPTIONS_BACK = Button(image=None, pos=(ANCHO_VENTANA/2, 250), 
                                text_input="Play", font=get_font(75), base_color="Black", hovering_color=(20,120,0))
            
            MEIN_MENU_BUTTON = Button(image=None, pos=(ANCHO_VENTANA/2, 300), 
                                text_input="Menu", font=get_font(75), base_color="Black", hovering_color=(20,120,0))
            
            VOLUME_MAS = Button(image=None, pos=(ANCHO_VENTANA/1.5, 350), 
                                text_input="+", font=get_font(75), base_color="Black", hovering_color=(20,120,0))
            
            VOLUME_MENOS = Button(image=None, pos=(360, 350), 
                                text_input="-", font=get_font(75), base_color="Black", hovering_color=(20,120,0))
            
            RANKING = Button(image=None, pos=(ANCHO_VENTANA/2, 450), 
                                text_input="Score", font=get_font(75), base_color="Black", hovering_color=(20,120,0))
            
            DIFICULTY_1 = Button(image=None, pos=(200, 530), 
                                text_input="Dificultad Facil", font=get_font(65), base_color="Black", hovering_color=(20,120,0))
            
            DIFICULTY_2 = Button(image=None, pos=(550, 530), 
                                text_input="Dificultad Media", font=get_font(65), base_color="Black", hovering_color=(20,120,0))
            
            DIFICULTY_3 = Button(image=None, pos=(900, 530), 
                                text_input="Dificultar Alta", font=get_font(65), base_color="Black", hovering_color=(20,120,0))

            for button in [OPTIONS_BACK,MEIN_MENU_BUTTON,VOLUME_MAS,VOLUME_MENOS,RANKING,DIFICULTY_1,DIFICULTY_2,DIFICULTY_3]:
                button.changeColor(OPTIONS_MOUSE_POS)
                button.update(pantalla)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                        self.play()
                        opciones = False
                    if MEIN_MENU_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                        self.main_menu()
                        opciones = False
                    if VOLUME_MAS.checkForInput(OPTIONS_MOUSE_POS):
                        if self.volumen < 0.9:
                            self.volumen += 0.1
                    if VOLUME_MENOS.checkForInput(OPTIONS_MOUSE_POS):
                        if self.volumen > 0.1:
                            self.volumen -= 0.1
                    if RANKING.checkForInput(OPTIONS_MOUSE_POS):
                        self.rankings()
                        opciones = False
                    if DIFICULTY_2.checkForInput(OPTIONS_MOUSE_POS):
                        self.dificultad = "dificultad_2"
                        print("cambios updateados")
                    if DIFICULTY_3.checkForInput(OPTIONS_MOUSE_POS):
                        self.dificultad = "dificultad_3"
                        print("cambios updateados")

            pygame.display.update()
    
    def play(self):  
        if not self.opciones:
            self.iniciar_juego()
        self.game.cargar_nuevas_configs(self.dificultad)
        print(self.dificultad)
        play_music(self.volumen,0, "Renders\Arabesque.mp3")
        playing = True
        while playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.options()
                        playing = False
            if self.game.perdiste == True:
                self.you_lost()
                playing = False
            
            delta_ms = clock.tick(60)
            pantalla.blit(self.game.fondo, (0,0))
            self.tiempo_transcurrido = self.game.get_tiempo()
            pantalla.blit(get_font(40).render(f"Tiempo: {self.tiempo_transcurrido}",True, "Black"), (10,10))
            vida = self.game.player_sprite.vida
            cord = 10
            for _ in range(vida//100):
                pantalla.blit(pygame.image.load("Renders\heart.png"),(cord, 40))
                cord += 20


            self.game.run(delta_ms)
            pygame.display.update()
            if self.dificultad == "dificultad_1":
                if self.tiempo_transcurrido > 19 and self.tiempo_transcurrido < 120:
                    self.dificultad = "dificultad_2"
                    print(self.dificultad)
            else:
                self.game.cargar_nuevas_configs(self.dificultad)
                if self.tiempo_transcurrido > 119:
                    self.dificultad = "dificultad_3"
                    self.game.cargar_nuevas_configs(self.dificultad)
                    print(self.dificultad)

    def you_lost(self):
        if self.game.perdiste==True:
            while True:
                pantalla.blit(self.game.fondo,(0,0))
                OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
                Texto = get_font(150).render("Game Over",True, "Black")
                pantalla.blit(Texto,(260,170))

                MEIN_MENU_BUTTON = Button(image=None, pos=(ANCHO_VENTANA/2, 400), 
                                text_input="Menu", font=get_font(75), base_color="Black", hovering_color=(20,120,0))
                RANKING = Button(image=None, pos=(ANCHO_VENTANA/2, 470), 
                                text_input="Score's", font=get_font(75), base_color="Black", hovering_color=(20,120,0))
                
                for button in [MEIN_MENU_BUTTON,RANKING]:
                    button.changeColor(OPTIONS_MOUSE_POS)
                    button.update(pantalla)

                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        if RANKING.checkForInput(OPTIONS_MOUSE_POS):
                            self.rankings()
                        if MEIN_MENU_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                            self.main_menu()
                        
                pygame.display.update()

    def rankings(self):
        while True:
            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
            pantalla.fill((0,0,0))

            MEIN_MENU_BUTTON = Button(image=None, pos=(ANCHO_VENTANA/2, 400), 
                            text_input="Menu", font=get_font(75), base_color="White", hovering_color=(20,120,0))
            
            RETURN = Button(image=None, pos=(ANCHO_VENTANA/2, 460), 
                                text_input="Return", font=get_font(75), base_color="White", hovering_color=(20,120,0))
            
            PLAY_AGAIN = Button(image=None, pos=(ANCHO_VENTANA/2, 520), 
                                text_input="Play Again", font=get_font(75), base_color="White", hovering_color=(20,120,0))
            
            for button in [MEIN_MENU_BUTTON,RETURN,PLAY_AGAIN]:
                    button.changeColor(OPTIONS_MOUSE_POS)
                    button.update(pantalla)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if MEIN_MENU_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                        self.main_menu()
                    if RETURN.checkForInput(OPTIONS_MOUSE_POS):
                        self.play()
                    if PLAY_AGAIN.checkForInput(OPTIONS_MOUSE_POS):
                        self.iniciar_juego()
                        self.play()
            try:
                Texto = get_font(80).render(f"Score: {self.game.player_sprite.puntaje}",True, "White")
                pantalla.blit(Texto,(380,170))
            except Exception:
                pass

            
            
            
            pygame.display.update()

    def iniciar_juego(self):
        self.game = Stage(pantalla, ANCHO_VENTANA, ALTO_VENTANA, self.dificultad)