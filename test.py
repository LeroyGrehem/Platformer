import sys

import pygame
from os import listdir
from os.path import isfile, join
from models import Player, Block, Fire, Button, Fruit

pygame.init()

pygame.display.set_caption("Platformer")

WIDTH, HEIGHT = 1000, 800
FPS = 60
PLAYER_VEL = 5

window = pygame.display.set_mode((WIDTH, HEIGHT))


def button_image(name):
    image = pygame.image.load(join("assets", "Menu", "Buttons", name)).convert_alpha()
    return image


def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites


def get_block(size):
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 0, size, size)
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


def draw_menu(window, background, bg_image, buttons):
    for tile in background:
        window.blit(bg_image, tile)
    for buttn in buttons:
        buttn.draw(window)
    pygame.display.update()


def draw_game(window, background, bg_image, player, objects, fruits, buttons, offset_x):
    for tile in background:
        window.blit(bg_image, tile)
    for obj in objects:
        obj.draw(window, offset_x)
    for button in buttons:
        button.draw(window)
    for fruit in fruits:
        fruit.draw(window, offset_x)

    player.draw(window, offset_x)

    pygame.display.update()


def wall_jump(player, objects):
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if player.rect.left == obj.rect.right:
                player.slide()


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


def start_game(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Purple.png")

    block_size = 94
    COLOR_PINK = (50, 141, 168)
    FONT = pygame.font.SysFont('Verdana', 20)
    back_button = Button(10, 20, button_image("Back.png"), 2.8)
    player = Player(100, 100, 50, 50)
    fire = Fire(150, HEIGHT - block_size - 64, 16, 32)
    fire.on()
    score = 0
    scroll_area_width = 200

    floor = [Block(i * block_size, HEIGHT - block_size, block_size)
             for i in range(-WIDTH // block_size, WIDTH * 2 // block_size)]
    roof = [Block(i * 54, 0, 54)
            for i in range(-WIDTH // 54, WIDTH * 2 // 54)]
    #
    # left_wall = [Block(-1056, i * block_size, block_size)
    #              for i in range((block_size * 2) , HEIGHT - (block_size * 2))]
    # blocks = [Block(0, HEIGHT - block_size, block_size)]
    objects = [*floor, *roof, Block(0, HEIGHT - block_size * 2, block_size),
               Block(block_size * 3, HEIGHT - block_size * 4, block_size),
               Block(block_size * 4, HEIGHT - block_size * 4, block_size),
               Block(block_size * 5, HEIGHT - block_size * 4, block_size),
               Block(block_size * 5, HEIGHT - block_size * 5, block_size),
               Block(block_size * 5, HEIGHT - block_size * 6, block_size), fire]
    buttons = [back_button]

    fruits = [Fruit(block_size * 3, HEIGHT - block_size * 5, 32, 32),
              Fruit(block_size * 4, HEIGHT - block_size * 5, 32, 32)]

    offset_x = 0



    run = True
    while run:

        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.draw(window):
                    start_menu(window)
                    # SCORE = 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and player.jump_count < 2:
                    player.jump()

        player.loop(FPS)
        fire.loop()
        for fruit in fruits:
            fruit.loop()
            if fruit.rect.colliderect(player):
                fruit.collected()
                if fruit.animation_count == 9:
                    score += 1
                    fruits.remove(fruit)

        handle_move(player, objects)

        draw_game(window, background, bg_image, player, objects, fruits, buttons, offset_x)

        if (player.rect.right - offset_x >= WIDTH - scroll_area_width and player.x_vel > 0) or (
                player.rect.left - offset_x <= scroll_area_width and player.x_vel < 0):
            offset_x += player.x_vel
        window.blit(FONT.render(str(score), True, COLOR_PINK), (WIDTH - 50, 20))
        print(player.rect)
        pygame.display.update()

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
