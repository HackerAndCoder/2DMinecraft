from settings import *
from utils import *
from chunk_handler import *

class World:
    def __init__(self):
        self.blocks = {}
        self.max_height = MAX_WORLD_HEIGHT
        self.generated_chunks = []

    def add_block(self, block : Block, pos = (0, 0)):
        pos = translate_pos(pos)
        self.blocks[pos] = block

    def remove_block(self, pos):
        pos = translate_pos(pos)
        try:
            del self.blocks[pos]
        except: # that block doesn't exist
            pass
    
    def get_block(self, pos):
        pos = translate_pos(pos)
        try:
            return self.blocks[pos]
        except:
            return None
    
    def get_highest_point(self, x_coord):
        tallest_so_far = 0
        for key in self.blocks.keys():
            if key[0] == x_coord:
                maybe = translate_y_axis(key[1])
                if maybe > tallest_so_far:
                    tallest_so_far = maybe
        return int(tallest_so_far)
    
    def gen_chunk(self, chunk_offset = 0):
        if chunk_offset in self.generated_chunks:
            # maybe load the chunk from a save file or something here
            return
        self.generated_chunks.append(chunk_offset)
        chunk = WorldGenerator.gen_chunk(chunk_offset)
        self.blocks = merge(self.blocks, chunk.blocks)
