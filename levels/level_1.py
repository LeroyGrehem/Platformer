import pygame

from os.path import join, isfile
from game import window, get_block, get_background
from models import Player, Block, Fire, Button, Fruit


def run_lvl_1(window):

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
