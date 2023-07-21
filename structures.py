from blocks import *


class Structure:
    def get_blocks():
        return {}

class Tree(Structure):
    def get_blocks():
        return  {
                    (0, 0): LOG,
                    (0, 1): LOG
                }