# Settings and constants
TITLE = 'Doody Jump'
WIDTH = 480
HEIGHT = 600
FPS = 60

# Player properties
PLAYER_ACCELERATION = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAVITY = 0.8
PLAYER_JUMP = 20

# Layers
PLAYER_LAYER = 2
MOB_LAYER = 2
PLATFORM_LAYER = 1
POWERUP_LAYER = 1
CLOUD_LAYER = 0

# Starting platforms
PLATFORM_LIST = [(0, HEIGHT - 60),
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4),
                 (125, HEIGHT - 350),
                 (350, 200),
                 (175, 100)]

# Game properties
BOOST_POWER = 60
POW_SPAWN_PCT = 7
MOB_FREQ = 5000

# Color definitions
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (0, 155, 155)
BG_COLOR = LIGHT_BLUE

# Fonts
FONT_NAME = 'arial'

# External files
HIGH_SCORE_FILE = 'highscore.txt'
SPRITE_SHEET = 'spritesheet_jumper.png'
