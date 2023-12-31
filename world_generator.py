from settings import *
import random, chunk_handler, yaml, utils
from blocks import *


class WorldGenerator:
    def gen_y_column(x, amplifier = 1, max_height = MAX_WORLD_HEIGHT // 2):
        #blocks = list(GRASS for i in range(max_height))
        blocks = []
        height = world_generator.one(x * amplifier ) + 1.5 * (max_height)
        if height < 5:
            height = 5
        for y in range(int(height)):
            blocks.append(STONE)

        try:
            blocks[0] = BEDROCK
        except:
            pass
        
        try:
            for y in range(random.randint(2, 3)):
                y += 1
                blocks[-y] = DIRT
        except:
            pass
        
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
            for c in range(len(ore_config)):
                config = ore_config[c]
                for gen in range(config['gens-per-chunk']):
                    gen_location_x = random.randint(0, CHUNK_SIZE) + offset_in_chunks * CHUNK_SIZE
                    gen_location_y = utils.translate_y_axis(random.randint(config['min-y'], config['max-y']))
                    for i in range(random.randint(config['min-vein-size'], config['max-vein-size'])):
                        if (gen_location_x, gen_location_y) in blocks.keys():
                            if blocks[(gen_location_x, gen_location_y)] == STONE:
                                blocks[(gen_location_x, gen_location_y)] = ore
                                next_location = utils.get_random_coord_around(gen_location_x, gen_location_y)
                                gen_location_x, gen_location_y = next_location[0], next_location[1]


        chunk = chunk_handler.Chunk()
        chunk.blocks = blocks
        return chunk