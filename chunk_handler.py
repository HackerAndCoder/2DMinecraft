import blocks
from settings import *
from world_generator import *

def translate_y_axis(coord : int):
    return MAX_WORLD_HEIGHT - coord

def translate_pos(pos = (0, 0)):
    return (pos[0], translate_y_axis(pos[1]))


class Chunk:
    def __init__(self):
        self.blocks = {}
    
    def get_highest_point(x_coord, dict_of_blocks):
        tallest_so_far = 0
        for key in dict_of_blocks.keys():
            if key[0] == x_coord:
                maybe = translate_y_axis(key[1])
                if maybe > tallest_so_far:
                    tallest_so_far = maybe
        return int(tallest_so_far)

    def generate(self, offset_in_chunks = 0):

        return WorldGenerator.gen_chunk(offset_in_chunks).blocks

