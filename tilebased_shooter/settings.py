import pygame as pg
vector = pg.math.Vector2

# Color definitions
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GREY = (40, 40, 40)
LIGHT_GREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)

# Game settings
WIDTH = 1024
HEIGHT = 768
FPS = 60
TITLE = 'TILE BASED GAME'
BG_COLOR = BROWN

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

WALL_IMAGE = 'tileGreen_39.png'

# Mob settings
MOB_HEALTH = 100
MOB_IMAGE = 'zoimbie1_hold.png'
MOB_SPEEDS = [150, 100, 75, 125]
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
MOB_DMG = 10
MOB_KNOCKBACK = 20
MOB_AVOID_RAD = 50
MOB_DETECT_RAD = 400

# Weapons Settings
BULLET_IMG = 'bullet.png'
WEAPONS = {}
WEAPONS['pistol'] = {
    'bullet_speed': 500,
    'bullet_lifetime': 1000,
    'bullet_rate': 250,
    'kickback': 200,
    'spread': 5,
    'damage': 10,
    'bullet_size': 'lg',
    'bullet_count': 1
}
WEAPONS['shotgun'] = {
    'bullet_speed': 400,
    'bullet_lifetime': 500,
    'bullet_rate': 900,
    'kickback': 300,
    'spread': 20,
    'damage': 10,
    'bullet_size': 'sm',
    'bullet_count': 12
}

# Player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 300
PLAYER_ROT_SPEED = 250
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
PLAYER_IMAGE = 'manBlue_gun.png'
BARREL_OFFSET = vector(25, 10)

# Effects
MUZZLE_FLASHES = ['whitePuff15.png', 'whitePuff16.png', 'whitePuff17.png',
                  'whitePuff18.png']
FLASH_DURATION = 40
SPLAT_IMG = 'splat green.png'
DMG_ALPHA = [i for i in range(0, 255, 25)]

# Layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEM_LAYER = 1

# Items
ITEM_IMAGES = {
    'health': 'health_pack.png',
    'shotgun': 'obj_shotgun.png'
}
HEALTH_PACK_AMOUNT = 20
BOB_RANGE = 15
BOB_SPEED = 0.4

# Sounds
BG_MUSIC = 'espionage.ogg'
PLAYER_HIT_SOUNDS = ['pain/8.wav', 'pain/9.wav', 'pain/10.wav', 'pain/11.wav']
ZOMBIE_MOAN_SOUNDS = ['brains2.wav', 'brains3.wav', 'zombie-roar-1.wav', 'zombie-roar-2.wav',
                      'zombie-roar-3.wav', 'zombie-roar-5.wav', 'zombie-roar-6.wav', 'zombie-roar-7.wav']
ZOMBIE_HIT_SOUNDS = ['splat-15.wav']
WEAPON_SOUNDS = {
    'pistol': ['pistol.wav'],
    'shotgun': ['shotgun.wav']
}
EFFECTS_SOUNDS = {
    'level_start': 'level_start.wav',
    'health_up': 'health_pack.wav',
    'gun_pickup': 'gun_pickup.wav'
}