# Sprite classes
import pygame as pg
from platformer.settings import *
import random
vector = pg.math.Vector2


class Spritesheet:
    # utility class for loading and parsing sprite sheets
    def __init__(self, filename):
        self.sprite_sheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab a sub texture out of the sprite sheet
        image = pg.Surface((width, height))
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (int(width / 2), int(height / 2)))
        image.set_colorkey(BLACK)
        return image


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        # animation variables
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0

        # image variables
        self.standing_frames = []
        self.walking_frames_l = []
        self.walking_frames_r = []
        self.jump_frame = None
        self.load_images()
        self.image = self.standing_frames[0]

        # rect variables
        self.rect = self.image.get_rect()
        self.rect.center = (40, HEIGHT - 100)

        # movement variables
        self.position = vector(40, HEIGHT - 100)
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)

    def update(self):
        self.animate()
        self.acceleration = vector(0, PLAYER_GRAVITY)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acceleration.x = -PLAYER_ACCELERATION
        if keys[pg.K_RIGHT]:
            self.acceleration.x = PLAYER_ACCELERATION

        # apply friction to x axis (not y because gravity)
        self.acceleration.x += self.velocity.x * PLAYER_FRICTION
        # equations of motion
        self.velocity += self.acceleration
        if abs(self.velocity.x) < 0.1:
            self.velocity.x = 0
        self.position += self.velocity + 0.5 * self.acceleration
        # wrap around screen edges
        if self.position.x > WIDTH + self.rect.width / 2:
            self.position.x = 0 - self.rect.width / 2
        if self.position.x < 0 - self.rect.width / 2:
            self.position.x = WIDTH + self.rect.width / 2

        # reposition rectangle on new position
        self.rect.midbottom = self.position

    def jump(self):
        self.rect.x += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 2
        if hits and not self.jumping:
            self.game.jump_sound.play()
            self.jumping = True
            self.velocity.y = -PLAYER_JUMP

    def end_jump(self):
        if self.jumping:
            if self.velocity.y < -3:
                self.velocity.y = -3

    def animate(self):
        now = pg.time.get_ticks()
        if not self.velocity.x == 0:
            self.walking = True
        else:
            self.walking = False

        # walking animation
        if self.walking:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames_l)
                bottom = self.rect.bottom
                if self.velocity.x > 0:
                    self.image = self.walking_frames_r[self.current_frame]
                else:
                    self.image = self.walking_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # idle animation
        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # jumping animation
        if self.jumping:
            bottom = self.rect.bottom
            self.image = self.jump_frame
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

        self.mask = pg.mask.from_surface(self.image)

    def load_images(self):
        self.standing_frames.append(self.game.sprite_sheet.get_image(614, 1063, 120, 191))
        self.standing_frames.append(self.game.sprite_sheet.get_image(690, 406, 120, 201))

        self.walking_frames_r.append(self.game.sprite_sheet.get_image(678, 860, 120, 201))
        self.walking_frames_r.append(self.game.sprite_sheet.get_image(692, 1458, 120, 207))

        for frame in self.walking_frames_r:
            self.walking_frames_l.append(pg.transform.flip(frame, True, False))

        self.jump_frame = self.game.sprite_sheet.get_image(382, 763, 150, 181)


class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLATFORM_LAYER
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        images = [
            self.game.sprite_sheet.get_image(0, 288, 380, 94),
            self.game.sprite_sheet.get_image(213, 1662, 201, 100)
        ]
        self.image = random.choice(images)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if random.randrange(100) < POW_SPAWN_PCT:
            Powerup(self.game, self )


class Powerup(pg.sprite.Sprite):
    def __init__(self, game, platform):
        self._layer = POWERUP_LAYER
        self.groups = game.all_sprites, game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.platform = platform
        self.type = random.choice(['boost'])
        self.image = self.game.sprite_sheet.get_image(820, 1805, 71, 70)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.platform.rect.centerx
        self.rect.bottom = self.platform.rect.top - 5

    def update(self):
        self.rect.bottom = self.platform.rect.top - 5
        if not self.game.platforms.has(self.platform):
            self.kill()


class Mob(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image_up = self.game.sprite_sheet.get_image(566, 510, 122, 139)
        self.image_down = self.game.sprite_sheet.get_image(568, 1534, 122, 135)
        self.image = self.image_up
        self.rect = self.image.get_rect()
        self.rect.centerx = random.choice([-100, WIDTH + 100])
        self.velocity_x = random.randrange(1, 4)
        if self.rect.centerx > WIDTH:
            self.velocity_x *= -1
        self.rect.y = random.randrange(HEIGHT / 2)
        self.velocity_y = 0
        self.duration_y = 0.5

    def update(self):
        self.rect.x += self.velocity_x
        self.velocity_y += self.duration_y
        if self.velocity_y > 3 or self.velocity_y < -3:
            self.duration_y *= -1

        center = self.rect.center
        if self.duration_y < 0:
            self.image = self.image_up
        else:
            self.image = self.image_down
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.rect.center = center

        self.rect.y += self.velocity_y
        if self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()


class Cloud(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = CLOUD_LAYER
        self.groups = game.all_sprites, game.clouds
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = random.choice(self.game.cloud_images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        scale = random.randrange(50, 101) / 100
        self.image = pg.transform.scale(self.image, (int(self.rect.width * scale), int(self.rect.height * scale)))
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-500, -50)

    def update(self):
        if self.rect.top > HEIGHT * 2:
            self.kill()