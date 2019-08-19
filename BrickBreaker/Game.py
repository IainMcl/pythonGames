import pygame
from pygame.locals import *
from Platform import Platform
from Ball import Ball

class Game(object):
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Brick Breaker")
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load("background.jpg")
        self.win = pygame.display.set_mode((500,500), HWSURFACE|DOUBLEBUF|RESIZABLE)
        self.win.blit(pygame.transform.scale(self.background, pygame.display.get_surface().get_size()), (0, 0))
        self.width, self.height = pygame.display.get_surface().get_size()

    def gameLoop(self):
        playing = True
        platform = Platform(self.width, self.height)
        ball = Ball(self.width, self.height)
        object_list = [platform, ball]
        while playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == VIDEORESIZE:
                    self.win = pygame.display.set_mode(event.dict['size'], HWSURFACE|DOUBLEBUF|RESIZABLE)
                    self.win.blit(pygame.transform.scale(self.background, event.dict['size']), (0, 0))
                    self.width, self.height = pygame.display.get_surface().get_size()
                    for obj in object_list:
                        if obj.width and obj.height:
                            obj.width = self.width 
                            obj.height = self.height
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                platform_dir = -1
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                platform_dir = 1
            else:
                platform_dir = 0
            
            platform.move(platform_dir)
            pygame.display.update()
