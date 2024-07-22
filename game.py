import os
import pygame
import os
import sys
from os import listdir
from os.path import isfile, join
from models import *

pygame.init()

pygame.display.set_caption("Platformer")

WIDTH, HEIGHT = 1000, 800
FPS = 60
PLAYER_VEL = 5

window = pygame.display.set_mode((WIDTH, HEIGHT))


def button_image(name):
    image = pygame.image.load(join("assets", "Menu", "Buttons", name)).convert_alpha()
    return image


def get_block(size):
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(272, 64, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)


def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []
    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)
    return tiles, image


def draw(window, background, bg_image, player, objects, offset_x):
    for tile in background:
        window.blit(bg_image, tile)
    for obj in objects:
        obj.draw(window, offset_x)

    player.draw(window, offset_x)

    pygame.display.update()


def handle_vertical_collision(player, objects, dy):
    collided_object = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_object.append(obj)
    return collided_object


def collide(player, object, dx):
    player.move(dx, 0)
    player.update()
    colidded_object = None
    for obj in object:
        if pygame.sprite.collide_mask(player, obj):
            colidded_object = obj
            break


    player.move(-dx, 0)
    player.update()
    return colidded_object


def handle_move(player, objects):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    collide_left = collide(player, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, objects, PLAYER_VEL * 2)

    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]
    for obj in to_check:
        if obj and obj.name == "fire":
            player.make_hit()


def draw_menu(window, background, bg_image, buttons):
    for tile in background:
        window.blit(bg_image, tile)
    for buttn in buttons:
        buttn.draw(window)
    pygame.display.update()


def start_game(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Purple.png")

    block_size = 96

    player = Player(100, 100, 50, 50)
    fire = Fire(100, HEIGHT - block_size - 64, 16, 32)
    fire.on()
    floor = [Block(i * block_size, HEIGHT - block_size, block_size)
             for i in range(-WIDTH // block_size, WIDTH * 2 // block_size)]
    # blocks = [Block(0, HEIGHT - block_size, block_size)]
    objects = [*floor, Block(0, HEIGHT - block_size * 2, block_size),
               Block(block_size * 3, HEIGHT - block_size * 4, block_size), fire]

    offset_x = 0
    scroll_area_width = 200

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and player.jump_count < 2:
                    player.jump()

        player.loop(FPS)
        fire.loop()
        handle_move(player, objects)
        draw(window, background, bg_image, player, objects, offset_x)

        if (player.rect.right - offset_x >= WIDTH - scroll_area_width and player.x_vel > 0) or (
                player.rect.left - offset_x <= scroll_area_width and player.x_vel < 0):
            offset_x += player.x_vel

    pygame.quit()
    quit()


def start_menu(window):
    background, bg_image = get_background("Blue.png")

    exit_button = Button(400, 200, button_image("Close.png"), 3.0)
    pinkman_button = Button(150, 400, button_image("Play.png"), 2.0)
    ninjafrog_button = Button(350, 400, button_image("Play.png"), 2.0)
    maskdude_button = Button(550, 400, button_image("Play.png"), 2.0)
    virtualguy_button = Button(850, 400, button_image("Play.png"), 2.0)

    buttons = [exit_button, pinkman_button, ninjafrog_button, maskdude_button, virtualguy_button]
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if pinkman_button.draw(window):
                    Player.select_character(window, "PinkMan")
                    start_game(window)
                if ninjafrog_button.draw(window):
                    Player.select_character(window, "NinjaFrog")
                    start_game(window)
                if maskdude_button.draw(window):
                    Player.select_character(window, "MaskDude")
                    start_game(window)
                if virtualguy_button.draw(window):
                    Player.select_character(window, "VirtualGuy")
                    start_game(window)

                if exit_button.draw(window):
                    pygame.quit()
                    print("Exit")
                    sys.exit()

        draw_menu(window, background, bg_image, buttons)


if __name__ == "__main__":
    start_menu(window)
