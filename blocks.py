import pygame, os, utils

class Block:
    def __init__(self, name = None):
        self.texture = utils.get_block_texture(name)
        self.name = name


GRASS = Block('grass_block')
STONE = Block('stone')
BEDROCK = Block('bedrock')
DIRT = Block('dirt')
LOG = Block('log')
LEAVES = Block('leaves')

COAL_ORE = Block('coal_ore')
GOLD_ORE = Block('gold_ore')
IRON_ORE = Block('iron_ore')
DIAMOND_ORE = Block('diamond_ore')

ORE_BLOCKS = [COAL_ORE, GOLD_ORE, IRON_ORE, DIAMOND_ORE]