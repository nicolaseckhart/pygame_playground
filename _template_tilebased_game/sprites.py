# Sprite classes
import pygame as pg
from _template_tilebased_game.settings import *
vector = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.vel = vector(0, 0)
        self.pos = vector(x, y) * TILESIZE

    def get_keys(self):
        self.vel = vector(0, 0)
        keys = pg.key.get_pressed()
        # to disable 8-way movement turn ifs 2-4 into elif
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED
        # make sure diagonal movement isn't faster than vertical / horizontal
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071

    def collide_with_walls(self, direction):
        if direction == 'x':
            collisions = pg.sprite.spritecollide(self, self.game.walls, False)
            if collisions:
                if self.vel.x > 0:
                    self.pos.x = collisions[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = collisions[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if direction == 'y':
            collisions = pg.sprite.spritecollide(self, self.game.walls, False)
            if collisions:
                if self.vel.y > 0:
                    self.pos.y = collisions[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = collisions[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y

    def update(self):
        self.get_keys()
        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE