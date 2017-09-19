import os
import sys
import pygame as pg
from _template_tilebased_game.settings import *
from _template_tilebased_game.sprites import *
from _template_tilebased_game.tilemap import *


class Game:
    def __init__(self):
        # initialize game window & clock
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)

        # initialize directories
        self.game_dir = os.path.dirname(__file__)
        self.img_dir = os.path.join(self.game_dir, 'img')
        self.snd_dir = os.path.join(self.game_dir, 'snd')
        self.map_dir = os.path.join(self.game_dir, 'map')

        # load image and sound data
        self.load_data()

        # define sprite groups
        self.all_sprites = None
        self.walls = None

        # define game variables
        self.running = True
        self.playing = False
        self.camera = None

    def load_data(self):
        self.map = Tilemap(os.path.join(self.map_dir, 'map.txt'))

    def new(self):
        # initialize sprite groups
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()

        # initialize sprites
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)

        # initialize camera with total map size
        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        # game loop
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # game loop - update section
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHT_GREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHT_GREY, (0, y), (WIDTH, y))

    def draw(self):
        # game loop - draw section
        self.screen.fill(BG_COLOR)
        self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()

    def events(self):
        # game loop - event management
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
