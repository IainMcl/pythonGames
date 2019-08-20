import pygame
import numpy as np
# from ScreenObject import ScreenObject ## Maybe use base classes

class Ball(object):
    def __init__(self, game_width, game_height):
        self.width = game_width
        self.height = game_height
        self.x = self.width // 2
        self.y = self.height // 2
        self.radius = None
        self.vx = 1
        self.vy = 1
        self.speed = 1
        self.resize(self.width, self.height)

    def resize(self, new_screen_width, new_screen_height):
        width_resize_ratio = new_screen_width / self.width
        height_resize_ratio = new_screen_height / self.height
        resize_ratio = np.sqrt(np.square(width_resize_ratio) + np.square(height_resize_ratio))
        self.x = int((self.x / self.width) * new_screen_width)
        self.y = int((self.y / self.height) * new_screen_height)
        self.vx *= width_resize_ratio
        self.vy *= height_resize_ratio        
        self.width = new_screen_width
        self.height = new_screen_height
        self.radius = self.width // 50
        self.speed *= resize_ratio

    def draw(self, win):
        pygame.draw.circle(win, (255, 20, 20), (int(self.x), int(self.y)), self.radius)
    
    def move(self):
        # if ball hits size wall then bounce
        if self.x - self.radius <= 0 or self.x + self.radius >= self.width:
            self.vx *= -1
        # If ball hits roof then bounce
        if self.y - self.radius <= 0:
            self.vy *= -1
        # If ball goes of the screen return 0 and stop
        if self.y - self.radius >= self.height:
            return 0
        # Update position
        self.x += self.vx * self.speed
        self.y += self.vy * self.speed
        return (self.x, self.y)

    def platformCollide(self, platform):
        if self.y + self.radius >= platform.y:
            if self.x + self.radius >= platform.x and self.x - self.radius <= platform.x + platform.platform_width:
                self.vy *= -1
                pos_on_plat = self.x - platform.x
                val = 1 - self.gaussian(pos_on_plat, platform.platform_width / 2, 1) * self.vx
                if (pos_on_plat < platform.platform_width / 2 and self.vx > 0) or (pos_on_plat > platform.platform_width / 2 and self.vx < 0):
                    self.vx *= -1
                if pos_on_plat == platform.platform_width // 2:
                    self.vx = 0
                self.vx *= val

    @staticmethod
    def gaussian(x, mu, sig):
        return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))
