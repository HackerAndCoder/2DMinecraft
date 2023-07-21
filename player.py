from utils import *

class Player:
    def __init__(self, x = 0, y = 0):
        self._x = x
        self._y = translate_y_axis(y - 64)
    
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
