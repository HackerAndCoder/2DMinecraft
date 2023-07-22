from utils import *
import pygame

class Player:
    def __init__(self, x = 0, y = 0):
        self._x = x
        self._y = translate_y_axis(y - 64)
        self.texture = resize_image(get_entity_texture('steve'), 16, 64)
        self.is_flying = False
        self.ticks_fallen = 0

    def set_x(self, x):
        self._x = x
    
    def set_y(self, y):
        self._y = translate_y_axis(y)
        #print(f'Normal y: {self._y}, Modified y: {128 - self._y}')

    def get_y(self):
        return translate_y_axis(self._y)
        #return 128 - self._y
    
    def get_x(self):
        return self._x
    
    def update(self):
        self.hitbox = pygame.Rect(self.get_x(), self.get_y() + 2, 1, 2)
    
    def get_pos(self):
        return (self.get_x(), self.get_y())
    
    def set_pos(self, pos):
        self.set_x(pos[0])
        self.set_y(pos[1])
