import perlin, random

MAX_WORLD_HEIGHT = 64
TREES_PER_CHUNK = 2
CHUNK_SIZE = 32
world_generator = perlin.Perlin(random.randint(0, 10000))
PLAYER_MOVE_SPEED = 0.3
ZOOM = 39 # originally was 40 but reducing it reduces the random white lines from rendering

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600