from settings import *
import pygame, os, yaml

def merge(dict1, dict2):
    return dict1 | dict2

def get_block_texture(name_hint, ZOOM = ZOOM):
    return pygame.transform.scale(pygame.image.load(os.path.join('assets', 'textures', 'blocks', name_hint + '.png')), (ZOOM, ZOOM))

def get_entity_texture(name_hint):
    return pygame.image.load(os.path.join('assets', 'textures', 'entities', name_hint + '.png')) 

def resize_image(image, resize_x, resize_y):
    return pygame.transform.scale(image, (resize_x, resize_y))

def translate_pos(pos1 = (0, 0), x_move = 0, y_move = 0):
    return (pos1[0] + x_move, pos1[1] + y_move)

def _is_on_screen(x, y, ZOOM = ZOOM):
    global SCREEN_WIDTH, SCREEN_HEIGHT
    if (x * ZOOM <  SCREEN_WIDTH) and (y * ZOOM < SCREEN_HEIGHT):
        return True
    return False

def is_on_screen(camera_x = 0, camera_y = 0, x = 0, y = 0, ZOOM = ZOOM):
    return _is_on_screen(x + camera_x, y + camera_y, ZOOM)

def translate_y_axis(coord : int):
    return MAX_WORLD_HEIGHT - coord

def translate_pos(pos = (0, 0)):
    return (pos[0], translate_y_axis(pos[1]))

def get_structure_block_list(structure, pos):
    blocks = structure.get_blocks()
    new_blocks = {}
    for key in blocks.keys():
        new_blocks[translate_pos(key, pos[0], pos[1])] = blocks[key]
    return new_blocks

def get_ore_gen_settings(ore_name):
    with open(os.path.join('assets', 'misc', 'ore_gen', ore_name + '.yml')) as f:
        return yaml.load(f.read(), yaml.Loader)

def get_coords_around(x, y):
    return (
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1),
        (x + 1, y + 1),
        (x + 1, y - 1),
        (x - 1, y + 1),
        (x - 1, y - 1)
    )

def get_random_coord_around(x, y):
    return random.choice(get_coords_around(x, y))