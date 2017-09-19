import pygame
import random
import os

# constants
WIDTH = 480
HEIGHT = 600
FPS = 60
POWERUP_TIME = 5000

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

FONT_ARIAL = pygame.font.match_font('arial')

# set up assets folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
snd_folder = os.path.join(game_folder, 'snd')

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Shoot \'em up!')
clock = pygame.time.Clock()


def draw_lives(surface, x, y, lives, image):
    image.set_colorkey(BLACK)
    for i in range(lives):
        image_rect = image.get_rect()
        image_rect.x = x + 30 * i
        image_rect.y = y
        surface.blit(image, image_rect)


def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(FONT_ARIAL, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


def spawn_mob():
    mob = Mob()
    all_sprites.add(mob)
    mobs.add(mob)


def draw_shield_bar(surface, x, y, percentage):
    if percentage < 0:
        percentage = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (percentage / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, GREEN, fill_rect)
    pygame.draw.rect(surface, GREEN, outline_rect, 2)


def show_game_over_screen():
    screen.blit(background, background_rect)
    draw_text(screen, 'SHMUP!', 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, 'Arrow keys move, space fires.', 22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, 'Press any key to begin!', 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


# sprite classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 20
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_timer = pygame.time.get_ticks()

    def update(self):
        # timeout for powerups
        now = pygame.time.get_ticks()
        if self.power >= 2 and now - self.power_timer > POWERUP_TIME:
            self.power -= 1
            self.power_timer = now

        # unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 20

        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def powerup(self):
        self.power += 1
        self.power_timer = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                random.choice(bullet_sounds).play()
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                random.choice(bullet_sounds).play()

    def hide(self):
        # hide player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = random.choice(mob_images)
        self.original_image.set_colorkey(BLACK)
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.speedx = 0
        self.speedy = 0
        self.spawn()
        self.rotation = 0
        self.rotation_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -50 or self.rect.right > WIDTH + 50:
            self.spawn()

    def spawn(self):
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedx = random.randrange(-2, 2)
        self.speedy = random.randrange(2, 6)

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rotation = (self.rotation + self.rotation_speed) % 360
            new_image = pygame.transform.rotate(self.original_image, self.rotation)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # destroy bullet if it goes off screen
        if self.rect.bottom < 0:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_animation[self.size][0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_animation[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_animation[self.size][self.frame]
                self.image.set_colorkey(BLACK)
                self.rect = self.image.get_rect()
                self.rect.center = center


class Powerup(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        # destroy powerup if it goes off screen
        if self.rect.top > HEIGHT:
            self.kill()

# load all game graphics
background = pygame.image.load(os.path.join(img_folder, 'starfield.png')).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(os.path.join(img_folder, 'playerShip1_orange.png')).convert()
player_icon = pygame.transform.scale(player_img, (25, 19))
bullet_img = pygame.image.load(os.path.join(img_folder, 'laserRed16.png')).convert()
mob_images = []
mob_list = ['meteorBrown_big1.png', 'meteorBrown_big2.png', 'meteorBrown_med1.png', 'meteorBrown_med3.png',
            'meteorBrown_small1.png', 'meteorBrown_small2.png', 'meteorBrown_tiny1.png']
for img in mob_list:
    mob_images.append(pygame.image.load(os.path.join(img_folder, img)).convert())

explosion_animation = {}
explosion_animation['lg'] = []
explosion_animation['sm'] = []
explosion_animation['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(os.path.join(img_folder, filename)).convert()
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_animation['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_animation['sm'].append(img_sm)

    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(os.path.join(img_folder, filename)).convert()
    explosion_animation['player'].append(img)
powerup_images = {}
powerup_images['shield'] = pygame.image.load(os.path.join(img_folder, 'shield_gold.png')).convert()
powerup_images['gun'] = pygame.image.load(os.path.join(img_folder, 'bolt_gold.png')).convert()

# load all game sounds
explosion_sounds = []
for snd in ['explosion1.wav', 'explosion2.wav']:
    explosion_sounds.append(pygame.mixer.Sound(os.path.join(snd_folder, snd)))
bullet_sounds = []
for snd in ['laser1.wav', 'laser2.wav', 'laser3.wav']:
    bullet_sounds.append(pygame.mixer.Sound(os.path.join(snd_folder, snd)))
player_explosion_sound = pygame.mixer.Sound(os.path.join(snd_folder, 'player_explosion.wav'))
pygame.mixer.music.load(os.path.join(snd_folder, 'background_music.ogg'))
pygame.mixer.music.set_volume(0.4)
powerup_shield_sound = pygame.mixer.Sound(os.path.join(snd_folder, 'powerup_shield.wav'))
powerup_gun_sound = pygame.mixer.Sound(os.path.join(snd_folder, 'powerup_gun.wav'))

# start background music
pygame.mixer.music.play(loops=-1)

# game loop
game_over = True
running = True
while running:
    if game_over:
        show_game_over_screen()
        game_over = False
        # initialize sprite groups
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()

        # initialize player sprite
        player = Player()
        all_sprites.add(player)

        # initialize mob sprites
        for i in range(8):
            spawn_mob()

        # initialize score
        score = 0

    # keep loop running at the right speed
    clock.tick(FPS)
    # process events / inputs
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # update
    all_sprites.update()

    # check if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 50 - hit.radius
        random.choice(explosion_sounds).play()
        explosion = Explosion(hit.rect.center, 'lg')
        all_sprites.add(explosion)
        if random.randrange(100) > 96:
            powerup = Powerup(hit.rect.center)
            all_sprites.add(powerup)
            powerups.add(powerup)
        spawn_mob()

    # check if player was hit by mob
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        explosion = Explosion(hit.rect.center, 'sm')
        all_sprites.add(explosion)
        spawn_mob()
        if player.shield <= 0:
            player_explosion_sound.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100

    # check if player hit a powerup
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            powerup_shield_sound.play()
            player.shield += 20
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            powerup_gun_sound.play()
            player.powerup()


    # if the player died and the death animation has ended
    if player.lives == 0 and not death_explosion.alive():
        game_over = True

    # draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 20, WIDTH / 2, 10)
    draw_shield_bar(screen,  5, 5, player.shield)
    draw_lives(screen, WIDTH-100, 5, player.lives, player_icon)

    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()