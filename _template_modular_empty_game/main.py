import os
import random
import pygame as pg
from _template_modular_empty_game.settings import *
from _template_modular_empty_game.sprites import *

class Game:
    def __init__(self):
        # initialize game window & clock
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()

        # initialize directories
        game_dir = os.path.dirname(__file__)
        img_dir = os.path.join(game_dir, 'img')
        snd_dir = os.path.join(game_dir, 'snd')

        # initialize game variables
        self.running = True
        self.playing = False
        self.all_sprites = None
        self.player = None

    def new(self):
        # reinitialize game / start new game
        self.all_sprites = pg.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)
        self.run()

    def run(self):
        # game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # game loop - update section
        self.all_sprites.update()

    def events(self):
        # game loop - event handling section
        # process events / inputs
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        # game loop - draw section
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        pass

    def show_gameover_screen(self):
        pass

    def draw_text(self, text, size, x, y):
        font = pg.font.Font(FONT_ARIAL, size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

game = Game()
game.show_start_screen()
while game.running:
    game.new()
    game.show_gameover_screen()

pg.quit()
