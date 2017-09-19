# Sprite classes
import pygame as pg
from _template_modular_empty_game.settings import *


class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((30, 40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x_velocity = 0
        self.y_velocity = 0

    def update(self):
        self.x_velocity = 0
        self.y_velocity = 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.x_velocity = -5
        if keys[pg.K_RIGHT]:
            self.x_velocity = 5
        if keys[pg.K_UP]:
            self.y_velocity = -5
        if keys[pg.K_DOWN]:
            self.y_velocity = 5

        self.rect.x += self.x_velocity
        self.rect.y += self.y_velocity