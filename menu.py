import pygame
from os.path import join
from models import Fruit
from game import window, get_background

fruit = Fruit(100, 100, 32, 32)

fruit.get_len()


def collide(self, xvel, yvel, platforms):
    for p in platforms:
        if pygame.sprite.collide_rect(self, p):

            if xvel > 0:
                self.rect.right = p.rect.left
                self.onWall = True

            if xvel < 0:
                self.rect.left = p.rect.right
                self.onWall = True

            if yvel > 0:
                self.rect.bottom = p.rect.top
                self.onGround = True
                self.onWall = False
                self.yvel = 0
            if yvel < 0: self.rect.top = p.rect.bottom

            if self.onWall:
                self.yvel = 3

