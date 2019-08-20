import pygame 

class Platform(object):
    def __init__(self, game_width, game_height):
        self.width = game_width
        self.height = game_height
        self.x = None
        self.y = None
        self.platform_height = None
        self.platform_width = None
        self.speed = 5
        self.resize(self.width, self.height)

    def resize(self, new_scree_width, new_screen_height):
        width_resize_ratio = new_scree_width / self.width
        self.width = new_scree_width
        self.height = new_screen_height
        self.x = self.width // 2
        self.y = self.height - (self.height // 10)
        self.platform_width = self.width // 5
        self.platform_height = self.height // 50 
        self.speed *= width_resize_ratio

    def move(self, direction):
        # Direction = 1 move right; -1 move left
        self.x += self.speed * direction
        if self.x + self.platform_width >= self.width:
            self.x = self.width - self.platform_width
        if self.x <= 0:
            self.x = 0

    def draw(self, win):
        pygame.draw.rect(win, (255,255,255), (self.x, self.y, self.platform_width, self.platform_height))
        