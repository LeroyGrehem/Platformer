import os
import sys
import pygame
import random
import math
from os import listdir
from os.path import isfile, join
from models import *



pygame.init()

pygame.display.set_caption("Test")

WIDTH, HEIGHT = 1000, 800
FPS = 60
PLAYER_VEL = 5
BG_COLOR = (0, 0, 0)
BUTTON_COLOR = (100, 100, 100)


window = pygame.display.set_mode((WIDTH, HEIGHT))

def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []
    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)
    return tiles, image

def game_font(window):

    menu_size = (window.get_width, window.get_height)
    file_path = join("Menu", "Text", "Text(White) (8x10).png")
    menu_font = pygame.font.Font(file_path, 10)

# def character_area(w)

def start_menu(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png")

    run = True
    while run:
        return window


# if __name__ == "__main__":
    # start_game(window)