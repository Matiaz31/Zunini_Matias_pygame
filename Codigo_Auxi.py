import pygame
import math
import json
from Codigo_Button import Button
class SurfaceManager:
    @staticmethod
    def get_surface_from_spritesheet(img_path: str, cols: int, rows: int, step = 1, flip: bool = False) -> list[pygame.surface.Surface]:
        sprites_list = list()
        surface_img = pygame.image.load(img_path)
        frame_width = int(surface_img.get_width()/cols)
        frame_height = int(surface_img.get_height()/rows)

        for row in range(rows):

            for column in range(0, cols, step):
                x_axis = column * frame_width
                y_axis = row * frame_height

                frame_surface = surface_img.subsurface(
                    x_axis, y_axis, frame_width, frame_height
                )

                if flip:
                    frame_surface = pygame.transform.flip(frame_surface, True, False)
                sprites_list.append(frame_surface)
        return sprites_list
    
def move_coords(angle, radius, coords):
    theta = math.radians(angle)
    return coords[0] + radius * math.cos(theta), coords[1] + radius * math.sin(theta)

def get_font(size):
    return pygame.font.Font(None, size)

def open_configs() -> dict:
    with open("Json_data.json", "r", encoding="utf-8") as config:
        return json.load(config)
    
def play_music(suma,volumen, que):
    volumen += suma
    pygame.mixer.music.load(que)
    pygame.mixer.music.set_volume(volumen)
    pygame.mixer.music.play()

def quicksort_mayor(array):
    '''
    Recibe un array para iterar
    itera ordenando de menor a mayor'''
    if len(array) <= 1:
        return array
    else:
        pivot = array[0]
        menor = [x for x in array[1:] if x < pivot]
        mayor = [x for x in array[1:] if x >= pivot]
    return quicksort_mayor(mayor) + [pivot] + quicksort_mayor(menor)