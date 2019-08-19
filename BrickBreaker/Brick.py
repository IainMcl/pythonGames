import pygame

class Brick(object):
    def __init__(self, x, y, lives=1):
        self.x = x
        self.y = y
        self.lives = lives