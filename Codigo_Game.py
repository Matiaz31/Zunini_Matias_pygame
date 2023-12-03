import pygame
import sys
from Codigo_Stage import Stage
from Codigo_Assets import ANCHO_VENTANA, ALTO_VENTANA

class Game:
    def __init__(self) -> None:
        pass

    def run_stage(stage_name: str):
        pygame.init()
    
        screen = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        clock = pygame.time.Clock()
        game = Stage(screen, ANCHO_VENTANA, ALTO_VENTANA, stage_name)

        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.blit(game.fondo, (0,0))
            delta_ms = clock.tick(60)
            game.run(delta_ms)
            pygame.display.flip()
