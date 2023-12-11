import pygame
import sys
import sqlite3 as sql
from Codigo_Button import Button
from Codigo_Stage import Stage
from Codigo_Assets import ANCHO_VENTANA, ALTO_VENTANA
from Codigo_Auxi import get_font, play_music, quicksort_mayor
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "Base_de_datos.db")


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
        self.playing = False



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
                        self.menu = False
                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.options()
                        self.menu = False
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
                        self.opciones = False
                    if MEIN_MENU_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                        self.main_menu()
                        self.opciones = False
                    if VOLUME_MAS.checkForInput(OPTIONS_MOUSE_POS):
                        if self.volumen < 0.9:
                            self.volumen += 0.1
                    if VOLUME_MENOS.checkForInput(OPTIONS_MOUSE_POS):
                        if self.volumen > 0.1:
                            self.volumen -= 0.1
                    if RANKING.checkForInput(OPTIONS_MOUSE_POS):
                        self.rankings()
                        self.opciones = False
                    if DIFICULTY_1.checkForInput(OPTIONS_MOUSE_POS):
                        self.dificultad = "dificultad_1"
                        print("cambios updateados")
                    if DIFICULTY_2.checkForInput(OPTIONS_MOUSE_POS):
                        self.dificultad = "dificultad_2"
                        print("cambios updateados")
                    if DIFICULTY_3.checkForInput(OPTIONS_MOUSE_POS):
                        self.dificultad = "dificultad_3"
                        print("cambios updateados")

            pygame.display.update()
    
    def play(self):
        if not self.playing:
            self.iniciar_juego()
        self.playing = True

        self.game.cargar_nuevas_configs(self.dificultad)
        play_music(self.volumen,0, "Renders\Arabesque.mp3")

        playing = True
        while playing:
            delta_ms = clock.tick(60)
            pantalla.blit(self.game.fondo, (0,0))

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
            
            contador = 0
            momento_1 = pygame.time.get_ticks()//1000
            momento_2 = pygame.time.get_ticks()//1000 + 1
            if momento_2 != momento_1:
                contador += 1


            self.tiempo_transcurrido = pygame.time.get_ticks()//1000
            pantalla.blit(get_font(40).render(f"Tiempo: {contador}",True, "Black"), (10,10))
            pantalla.blit(get_font(40).render(f"Score: {self.game.player_sprite.puntaje}",True, "Black"), (160,10))

            vida = self.game.player_sprite.vida
            cord = 10
            for _ in range(vida//100):
                pantalla.blit(pygame.image.load("Renders\heart.png"),(cord, 40))
                cord += 20
            
            pygame.draw.line(pantalla, (0,0,0), (10,80), (100,80), 5)
            exp = self.game.player_sprite.exp
            pygame.draw.line(pantalla, "Blue", (10,80), (exp,80), 5)
            if self.game.player_sprite.level_up():
                self.upgrade()

            self.game.run(delta_ms)
            self.dificultades()
            pygame.display.update()

    def you_lost(self):
        if self.game.perdiste==True:
            while True:
                pantalla.blit(self.game.fondo,(0,0))
                OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
                Texto = get_font(150).render("Game Over",True, "Black")
                pantalla.blit(Texto,(260,170))

                MEIN_MENU_BUTTON = Button(image=None, pos=(ANCHO_VENTANA/2, 400), 
                                text_input="Menu", font=get_font(80), base_color="Black", hovering_color=(20,120,0))
                SET_RANKING = Button(image=None, pos=(ANCHO_VENTANA/2, 470), 
                                text_input="Guardar Score", font=get_font(80), base_color="Black", hovering_color=(20,120,0))
                PLAY_AGAIN = Button(image=None, pos=(ANCHO_VENTANA/2, 540), 
                                text_input="Play Again", font=get_font(80), base_color="Black", hovering_color=(20,120,0))
                
                for button in [MEIN_MENU_BUTTON,SET_RANKING,PLAY_AGAIN]:
                    button.changeColor(OPTIONS_MOUSE_POS)
                    button.update(pantalla)

                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        if SET_RANKING.checkForInput(OPTIONS_MOUSE_POS):
                            self.set_rankings()
                        if MEIN_MENU_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                            self.main_menu()
                        if PLAY_AGAIN.checkForInput(OPTIONS_MOUSE_POS):
                            self.iniciar_juego()
                            self.play()
                        
                pygame.display.update()

    def set_rankings(self):
        seteando = True
        tecla = pygame.transform.scale(pygame.image.load("Renders/tecla.png"),(50,50))
        lista_teclas = []
        while seteando:
            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
            pantalla.fill((0,0,0))

            Q_BUTTON = Button(image=tecla, pos=(50,200), 
                            text_input="Q", font=get_font(45), base_color="Black", hovering_color=(20,120,0))
            W_BUTTON = Button(image=tecla, pos=(100,200), 
                            text_input="W", font=get_font(45), base_color="Black", hovering_color=(20,120,0))
            E_BUTTON = Button(image=tecla, pos=(150,200), 
                            text_input="E", font=get_font(45), base_color="Black", hovering_color=(20,120,0))
            R_BUTTON = Button(image=tecla, pos=(200,200), 
                            text_input="R", font=get_font(45), base_color="Black", hovering_color=(20,120,0))
            T_BUTTON = Button(image=tecla, pos=(250,200), 
                            text_input="T", font=get_font(45), base_color="Black", hovering_color=(20,120,0))
            Y_BUTTON = Button(image=tecla, pos=(300,200), 
                            text_input="Y", font=get_font(45), base_color="Black", hovering_color=(20,120,0))
            U_BUTTON = Button(image=tecla, pos=(350,200), 
                            text_input="U", font=get_font(45), base_color="Black", hovering_color=(20,120,0))
            I_BUTTON = Button(image=tecla, pos=(400,200), 
                            text_input="I", font=get_font(45), base_color="Black", hovering_color=(20,120,0))
            O_BUTTON = Button(image=tecla, pos=(450,200), 
                            text_input="O", font=get_font(45), base_color="Black", hovering_color=(20,120,0))
            P_BUTTON = Button(image=tecla, pos=(500,200), 
                            text_input="P", font=get_font(45), base_color="Black", hovering_color=(20,120,0))
            A_BUTTON = Button(image=tecla, pos=(55,300), 
                            text_input="A", font=get_font(45), base_color="Black", hovering_color=(20,120,0))
            S_BUTTON = Button(image=tecla, pos=(105,300), 
                            text_input="S", font=get_font(45), base_color="Black", hovering_color=(20,120,0))
            D_BUTTON = Button(image=tecla, pos=(155,300), 
                            text_input="D", font=get_font(45), base_color="Black", hovering_color=(20,120,0))
            F_BUTTON = Button(image=tecla, pos=(205,300), 
                            text_input="F", font=get_font(45), base_color="Black", hovering_color=(20,120,0))
            G_BUTTON = Button(image=tecla, pos=(255,300), 
                            text_input="G", font=get_font(45), base_color="Black", hovering_color=(20,120,0))
            H_BUTTON = Button(image=tecla, pos=(305,300), 
                            text_input="H", font=get_font(45), base_color="Black", hovering_color=(20,120,0))
            J_BUTTON = Button(image=tecla, pos=(355,300), 
                            text_input="J", font=get_font(45), base_color="Black", hovering_color=(20,120,0))
            K_BUTTON = Button(image=tecla, pos=(405,300), 
                            text_input="K", font=get_font(45), base_color="Black", hovering_color=(20,120,0))
            L_BUTTON = Button(image=tecla, pos=(455,300), 
                            text_input="L", font=get_font(45), base_color="Black", hovering_color=(20,120,0))
            Ñ_BUTTON = Button(image=tecla, pos=(505,300), 
                            text_input="Ñ", font=get_font(45), base_color="Black", hovering_color=(20,120,0))
            Z_BUTTON = Button(image=tecla, pos=(60,400), 
                            text_input="Z", font=get_font(45), base_color="Black", hovering_color=(20,120,0))
            X_BUTTON = Button(image=tecla, pos=(110,400), 
                            text_input="X", font=get_font(45), base_color="Black", hovering_color=(20,120,0))
            C_BUTTON = Button(image=tecla, pos=(160,400), 
                            text_input="C", font=get_font(45), base_color="Black", hovering_color=(20,120,0))
            V_BUTTON = Button(image=tecla, pos=(210,400), 
                            text_input="V", font=get_font(45), base_color="Black", hovering_color=(20,120,0))
            B_BUTTON = Button(image=tecla, pos=(260,400), 
                            text_input="B", font=get_font(45), base_color="Black", hovering_color=(20,120,0))
            N_BUTTON = Button(image=tecla, pos=(310,400), 
                            text_input="N", font=get_font(45), base_color="Black", hovering_color=(20,120,0))
            M_BUTTON = Button(image=tecla, pos=(360,400), 
                            text_input="M", font=get_font(45), base_color="Black", hovering_color=(20,120,0))
            Go_BUTTON = Button(image=pygame.image.load("Renders\Options Rect.png"), pos=(600,600), 
                            text_input="Guardar", font=get_font(45), base_color="White", hovering_color=(20,120,0))
            
            for button in [Go_BUTTON,A_BUTTON,B_BUTTON,C_BUTTON,D_BUTTON,E_BUTTON,F_BUTTON,G_BUTTON,H_BUTTON,I_BUTTON,J_BUTTON,K_BUTTON,L_BUTTON,M_BUTTON,N_BUTTON,Ñ_BUTTON,O_BUTTON,P_BUTTON,Q_BUTTON,R_BUTTON,S_BUTTON,T_BUTTON,U_BUTTON,V_BUTTON,W_BUTTON,X_BUTTON,Y_BUTTON,Z_BUTTON]:
                button.changeColor(OPTIONS_MOUSE_POS)
                button.update(pantalla)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.play()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if Go_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                        if lista_teclas != []:
                            self.rankings()
                    if Q_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                        lista_teclas.append("Q")
                    if W_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                        lista_teclas.append("W")
                    if E_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                        lista_teclas.append("E")
                    if R_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                        lista_teclas.append("R")
                    if T_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                        lista_teclas.append("T")
                    if Y_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                        lista_teclas.append("Y")
                    if U_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                        lista_teclas.append("U")
                    if I_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                        lista_teclas.append("I")
                    if O_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                        lista_teclas.append("O")
                    if P_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                        lista_teclas.append("P")
                    if A_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                        lista_teclas.append("A")
                    if S_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                        lista_teclas.append("S")
                    if D_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                        lista_teclas.append("D")
                    if F_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                        lista_teclas.append("F")
                    if G_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                        lista_teclas.append("G")
                    if H_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                        lista_teclas.append("H")
                    if J_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                        lista_teclas.append("J")
                    if K_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                        lista_teclas.append("K")
                    if L_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                        lista_teclas.append("L")
                    if Ñ_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                        lista_teclas.append("Ñ")
                    if Z_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                        lista_teclas.append("Z")
                    if X_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                        lista_teclas.append("X")
                    if C_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                        lista_teclas.append("C")
                    if V_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                        lista_teclas.append("V")
                    if B_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                        lista_teclas.append("B")
                    if N_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                        lista_teclas.append("N")
                    if M_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                        lista_teclas.append("M")
                    
            self.nombre = "".join(lista_teclas)
            pantalla.blit(get_font(40).render(f"Nombre: {self.nombre}",True, "White"), (600,230))
            pygame.display.update()

    def rankings(self):
        rank = True
        self.sql()
        while rank:
            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
            pantalla.fill((0,0,0))

            MEIN_MENU_BUTTON = Button(image=None, pos=(ANCHO_VENTANA/2, 500), 
                            text_input="Menu", font=get_font(75), base_color="White", hovering_color=(20,120,0))
            RETURN = Button(image=None, pos=(ANCHO_VENTANA/2, 560), 
                                text_input="Return", font=get_font(75), base_color="White", hovering_color=(20,120,0))
            PLAY_AGAIN = Button(image=None, pos=(ANCHO_VENTANA/2, 620), 
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
                        rank = False
                        self.main_menu()
                    if RETURN.checkForInput(OPTIONS_MOUSE_POS):
                        rank = False
                        self.play()
                    if PLAY_AGAIN.checkForInput(OPTIONS_MOUSE_POS):
                        rank = False
                        self.iniciar_juego()
                        self.play()


            self.sql_blit()


            pygame.display.update()

    def upgrade(self):
        upgrading = True
        decimo = ANCHO_VENTANA/10
        while upgrading:
            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

            UPGRADE_1 = Button(image=pygame.image.load("Renders/velocidad.png"), pos=(decimo*2, ALTO_VENTANA/2), 
                            text_input="", font=get_font(45), base_color="White", hovering_color=(20,30,0))
            
            UPGRADE_2 = Button(image=pygame.image.load("Renders/vida.png"), pos=(decimo*5, ALTO_VENTANA/2), 
                                text_input="", font=get_font(45), base_color="White", hovering_color=(20,30,0))
            
            UPGRADE_3 = Button(image=pygame.image.load("Renders/espada.png"), pos=(decimo*8, ALTO_VENTANA/2), 
                                text_input="", font=get_font(45), base_color="White", hovering_color=(20,30,0))
            
            for button in [UPGRADE_1,UPGRADE_2,UPGRADE_3]:
                    button.changeColor(OPTIONS_MOUSE_POS)
                    button.update(pantalla)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if UPGRADE_1.checkForInput(OPTIONS_MOUSE_POS):
                        self.game.player_sprite.speed_walk += 0.5
                        self.play()
                    if UPGRADE_2.checkForInput(OPTIONS_MOUSE_POS):
                        self.game.player_sprite.vida += 100
                        self.play()
                    if UPGRADE_3.checkForInput(OPTIONS_MOUSE_POS):
                        self.game.player_sprite.daño_bala += 50
                        self.game.player_sprite.daño_flecha += 2
                        self.play()

           

            pygame.display.update()

    def iniciar_juego(self):
        self.game = Stage(pantalla, ANCHO_VENTANA, ALTO_VENTANA, self.dificultad)
    
    def dificultades(self):
        if self.dificultad == "dificultad_1":
            if self.tiempo_transcurrido > 59 and self.tiempo_transcurrido < 120:
                self.dificultad = "dificultad_2"
                print(self.dificultad)
        else:
            self.game.cargar_nuevas_configs(self.dificultad)
            if self.tiempo_transcurrido > 119 and self.tiempo_transcurrido < 201:
                self.dificultad = "dificultad_3"
                self.game.cargar_nuevas_configs(self.dificultad)
                print(self.dificultad)
            if self.tiempo_transcurrido > 200:
                self.dificultad = "dificultad_4"
                self.game.cargar_nuevas_configs(self.dificultad)
                print(self.dificultad)
                
    def sql(self):
        with sql.connect(db_path) as db:
            cursor = db.cursor()
            
            cursor.execute(
            """CREATE TABLE IF NOT EXISTS Score (   
            Nombres text,
            Scores text
            )
            """)
            db.commit()
            try:
                instruccion = f"INSERT INTO Score VALUES ('{self.nombre}', '{self.game.player_sprite.puntaje}')"
                cursor.execute(instruccion)
                db.commit()
            except Exception:
                pass

    def sql_blit(self):
        with sql.connect(db_path) as db:
            cursor = db.cursor()
        cursor.execute("SELECT Nombres, Scores FROM Score ORDER BY Scores")
        lista_ordenada =[]
        lista_desordenada =[]
        for fila in cursor:
            lista_desordenada.append(fila)
        lista_ordenada = quicksort_mayor(lista_desordenada)
        y = 80
        for fila in lista_ordenada:
            print(lista_ordenada)
            str_tabulado = f"NOMBRE: {fila[0]}, Score: {fila[1]}"
            if y < 400:
                pantalla.blit(get_font(50).render(f"NOMBRE: {fila[0]}, Score: {fila[1]}",True, "White"), (ANCHO_VENTANA/3,y))
            y += 50



    # def upgrade(self):
    #     upgrading = True
    #     decimo = ANCHO_VENTANA/10
    #     while upgrading:
    #         OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

    #         lista_upgrades = []
                
    #         carta_1 = (decimo*2, ALTO_VENTANA/2)
    #         carta_2 = (decimo*5, ALTO_VENTANA/2)
    #         carta_3 = (decimo*8, ALTO_VENTANA/2)
            
    #         upgrade_type_1 = ""
    #         upgrade_type_2 = ""
    #         upgrade_type_3 = ""
            
    #         if upgrade_type_1 == "":
    #             upgrade_type_1 = random.choice(["daño", "cooldawn", "score"])
    #         match upgrade_type_1:
    #             case "daño":
    #                 UPGRADE_daño = Button(image=pygame.image.load("Renders/espada.png"), pos=(carta_1), 
    #                             text_input="", font=get_font(45), base_color="Black", hovering_color=(20,30,0))
    #                 lista_upgrades.append(UPGRADE_daño)
    #             case "cooldawn":
    #                 UPGRADE_cooldawn = Button(image=pygame.image.load("Renders/ojo.png"), pos=(carta_1), 
    #                             text_input="", font=get_font(45), base_color="Black", hovering_color=(20,30,0))
    #                 lista_upgrades.append(UPGRADE_cooldawn)
    #             case "score":
    #                 UPGRADE_score = Button(image=pygame.image.load("Renders/emerald.png"), pos=(carta_1), 
    #                             text_input="", font=get_font(45), base_color="Black", hovering_color=(20,30,0))
    #                 lista_upgrades.append(UPGRADE_score)

    #         if upgrade_type_2 == "":
    #             upgrade_type_2 = random.choice(["cooldawn", "velocidad", "score"])
    #         match upgrade_type_2:
    #             case "cooldawn":
    #                 UPGRADE_cooldawn = Button(image=pygame.image.load("Renders/ojo.png"), pos=(carta_2), 
    #                             text_input="", font=get_font(45), base_color="Black", hovering_color=(20,30,0))
    #                 lista_upgrades.append(UPGRADE_cooldawn)
    #             case "velocidad":
    #                 UPGRADE_velocidad = Button(image=pygame.image.load("Renders/velocidad.png"), pos=(carta_2), 
    #                         text_input="", font=get_font(45), base_color="Black", hovering_color=(20,30,0))
    #                 lista_upgrades.append(UPGRADE_velocidad)
    #             case "score":
    #                 UPGRADE_score = Button(image=pygame.image.load("Renders/emerald.png"), pos=(carta_2), 
    #                             text_input="", font=get_font(45), base_color="Black", hovering_color=(20,30,0))
    #                 lista_upgrades.append(UPGRADE_score)

    #         if upgrade_type_3 == "":        
    #             upgrade_type_3 = random.choice(["velocidad", "vida", "score"])
    #         match upgrade_type_3:
    #             case "velocidad":
    #                 UPGRADE_velocidad = Button(image=pygame.image.load("Renders/velocidad.png"), pos=(carta_3), 
    #                         text_input="", font=get_font(45), base_color="Black", hovering_color=(20,30,0))
    #                 lista_upgrades.append(UPGRADE_velocidad)
    #             case "vida":
    #                 UPGRADE_vida = Button(image=pygame.image.load("Renders/vida.png"), pos=(carta_3), 
    #                             text_input="", font=get_font(45), base_color="Black", hovering_color=(20,30,0))
    #                 lista_upgrades.append(UPGRADE_vida)
    #             case "score":
    #                 UPGRADE_score = Button(image=pygame.image.load("Renders/emerald.png"), pos=(carta_3), 
    #                             text_input="", font=get_font(45), base_color="Black", hovering_color=(20,30,0))
    #                 lista_upgrades.append(UPGRADE_score)
            

    #         for evento in pygame.event.get():
    #             if evento.type == pygame.QUIT:
    #                 pygame.quit()
    #                 sys.exit()
    #             for button in lista_upgrades:
    #                 button.changeColor(OPTIONS_MOUSE_POS)
    #                 button.update(pantalla)
    #                 if evento.type == pygame.MOUSEBUTTONDOWN:
    #                     if button.checkForInput(OPTIONS_MOUSE_POS):
    #                         self.game.player_sprite.speed_walk += 0.5
    #                         self.play()
    #                     if button.checkForInput(OPTIONS_MOUSE_POS):
    #                         self.game.player_sprite.vida += 100
    #                         self.play()
    #                     if button.checkForInput(OPTIONS_MOUSE_POS):
    #                         self.game.player_sprite.daño_bala += 50
    #                         self.game.player_sprite.daño_flecha += 2
    #                         self.play()

    #         pygame.display.update()