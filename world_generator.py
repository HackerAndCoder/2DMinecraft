from settings import *
import random, chunk_handler, yaml, utils
from blocks import *

class WorldGenerator:
    def gen_y_column(x, amplifier = 1, max_height = MAX_WORLD_HEIGHT // 2):
        #blocks = list(GRASS for i in range(max_height))
        blocks = []
        height = world_generator.one(x * amplifier ) + 1 * (max_height)
        for y in range(height):
            blocks.append(STONE)

        try:
            blocks[0] = BEDROCK
        except:
            pass

        for y in range(random.randint(2, 3)):
            y += 1
            blocks[-y] = DIRT
        
        blocks[-1] = GRASS

        return blocks
    
    def gen_chunk(offset_in_chunks):
        blocks = {}
        for x in range(CHUNK_SIZE):
            yblocks = WorldGenerator.gen_y_column(x + offset_in_chunks * CHUNK_SIZE)
            for i in range(len(yblocks)):
                blocks[(offset_in_chunks * CHUNK_SIZE + x, MAX_WORLD_HEIGHT - i)] = yblocks[i]
        
        for ore in ORE_BLOCKS:
            ore_config = utils.get_ore_gen_settings(ore.name)
            for gen in range(ore_config['gens-per-chunk']):
                gen_location_x = random.randint(0, CHUNK_SIZE) + offset_in_chunks * CHUNK_SIZE
                gen_location_y = utils.translate_y_axis(random.randint(ore_config['min-y'], ore_config['max-y']))
                for i in range(random.randint(ore_config['min-vein-size'], ore_config['max-vein-size'])):
                    blocks[(gen_location_x, gen_location_y)] = ore
                    next_location = utils.get_random_coord_around(gen_location_x, gen_location_y)
                    gen_location_x, gen_location_y = next_location[0], next_location[1]

        chunk = chunk_handler.Chunk()
        chunk.blocks = blocks
        return chunk