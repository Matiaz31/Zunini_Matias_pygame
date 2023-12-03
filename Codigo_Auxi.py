import pygame
import math
import json


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