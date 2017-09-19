# Game class and main
from os import path
import random
import pygame as pg
from platformer.settings import *
from platformer.sprites import *


class Game:
    def __init__(self):
        # initialize game window & clock
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()

        # initialize directories
        self.game_dir = path.dirname(__file__)
        self.img_dir = path.join(self.game_dir, 'img')
        self.snd_dir = path.join(self.game_dir, 'snd')

        # initialize game variables
        self.font_name = pg.font.match_font(FONT_NAME)
        self.running = True
        self.playing = False
        self.player = None
        self.high_score = None
        self.score = None

        # load all assets and data
        self.load_data()

    def new(self):
        # set game variables for new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.clouds = pg.sprite.Group()

        self.mob_timer = 0

        # initialize score at 0
        self.score = 0

        # spawn sprites
        self.player = Player(self)
        for p in PLATFORM_LIST:
            Platform(self, *p)

        # load game music
        pg.mixer.music.load(path.join(self.snd_dir, 'background_music.ogg'))

        # spawn some clouds at the beginning
        for i in range(6):
            c = Cloud(self)
            c.rect.y += 500

        # jump into game loop
        self.run()

    def run(self):
        # start game music
        pg.mixer.music.play(loops=-1)

        # game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

        # end game music
        pg.mixer.music.fadeout(500)

    def update(self):
        # game loop - update section
        self.all_sprites.update()

        # spawn mobs
        now = pg.time.get_ticks()
        if now - self.mob_timer > 5000 + random.choice([-1000, -500, 0, 500, 1000]):
            self.mob_timer = now
            Mob(self)

        # check if player hits a mob
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, pg.sprite.collide_mask)
        if hits:
            self.playing = False

        # check if player hits a platform - only if falling
        if self.player.velocity.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.position.x < lowest.rect.right + 10 and self.player.position.x > lowest.rect.left - 10:
                    if self.player.position.y < lowest.rect.bottom:
                        self.player.position.y = lowest.rect.top + 1
                        self.player.velocity.y = 0
                        self.player.jumping = False

        # if player reaches top 4th of screen
        if self.player.rect.top <= HEIGHT / 4:
            if random.randrange(100) < 5:
                Cloud(self)

            self.player.position.y += max(abs(self.player.velocity.y), 5)
            for cloud in self.clouds:
                cloud.rect.y += max(abs(self.player.velocity.y / 2), 2)
            for mob in self.mobs:
                mob.rect.y += max(abs(self.player.velocity.y), 5)
            for platform in self.platforms:
                platform.rect.y += max(abs(self.player.velocity.y), 5)
                if platform.rect.top >= HEIGHT:
                    platform.kill()
                    # increase player score when platform pushed off screen
                    self.score += 10

        # spawn new platforms to keep constant amount
        while len(self.platforms) < 6:
            width = random.randrange(50, 100)
            Platform(self, random.randrange(0, WIDTH-width), random.randrange(-75, -30))

        # if player hits powerup
        hits = pg.sprite.spritecollide(self.player, self.powerups, True)
        for powerup in hits:
            if powerup.type == 'boost':
                self.boost_sound.play()
                self.player.velocity.y = -BOOST_POWER
                self.player.jumping = False

        # player death
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.velocity.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()

        if len(self.platforms) == 0:
            self.playing = False

    def events(self):
        # game loop - event handling section
        # process events / inputs
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.end_jump()

    def draw(self):
        # game loop - draw section
        self.screen.fill(BG_COLOR)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def load_data(self):
        # load high score (with context block closes after processing)
        with open(path.join(self.game_dir, HIGH_SCORE_FILE), 'w') as file:
            try:
                self.high_score = int(file.read())
            except:
                self.high_score = 0

        # load images
        self.sprite_sheet = Spritesheet(path.join(self.img_dir, SPRITE_SHEET))
        self.cloud_images = []
        for i in range(1, 4):
            self.cloud_images.append(pg.image.load(path.join(self.img_dir, 'cloud{}.png'.format(i))).convert())


        # load sounds
        self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir, 'jump1.wav'))
        self.boost_sound = pg.mixer.Sound(path.join(self.snd_dir, 'boost.wav'))

    def show_start_screen(self):
        pass
        self.screen.fill(BG_COLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text('Arrows to move and space to jump', 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text('Press any key to begin', 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text('High Score: ' + str(self.high_score), 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        if not self.running:
            return
        self.screen.fill(BG_COLOR)
        self.draw_text('GAME OVER', 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text('Score: ' + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text('Press any key to play again', 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        if self.score > self.high_score:
            self.high_score = self.score
            self.draw_text('NEW HIGH SCORE!', 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
            with open(path.join(self.game_dir, HIGH_SCORE_FILE), 'w') as file:
                file.write(str(self.score))
        else:
            self.draw_text('High Score: ' + str(self.high_score), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

game = Game()
game.show_start_screen()
while game.running:
    game.new()
    game.show_go_screen()

pg.quit()
