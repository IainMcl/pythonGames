import pygame

class Brick(object):
    def __init__(self, x, y, game_width, game_height, lives=1):
        self.x = x
        self.y = y
        self.width = game_width
        self.height = game_height
        self.brick_width = self.width // 2
        self.brick_height = self.height // 10
        self.lives = lives
        self.colour = self.getColour(lives)

    def getColour(self, index):
        colour_list = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        return colour_list[index]

    def resize(self, new_screen_width, new_screen_height):
        self.x = int((self.x / self.width) * new_screen_width)
        self.y = int((self.y / self.height) * new_screen_height)
        self.width = new_screen_width
        self.height = new_screen_height

    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.brick_width, self.brick_height))

    def brickHit(self):
        self.lives -= 1

    