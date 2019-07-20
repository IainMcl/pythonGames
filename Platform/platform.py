import numpy as np
import pygame

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Platform Game")
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load("background.jfif")
        self.size = self.background.get_rect().size
        self.win = pygame.display.set_mode((self.size[0], self.size[1]))
        if not self.background:
            print("Image not loaded")
            exit()
        self.game_loop()

    def game_loop(self):
        running = True
        objects = []
        player = Player(self.win, 168, 50)
        objects.append(player)
        while running:
            self.clock.tick(27)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                player.direction = 1
                player.vx = 1
            if keys[pygame.K_LEFT]:
                player.direction = -1
                player.vx = -1
            if keys[pygame.K_UP]:
                player.vy = -2
            if keys[pygame.K_DOWN]:
                player.vy = 2
                if player.onGround:
                    player.direction = 0
                    player.vx = 0
            self.draw(objects)

    def draw(self, objects):
        self.win.blit(self.background, (0,0))
        for obj in objects:
            obj.draw()
            obj.move()
        pygame.display.update()
        
        
class MovingObject(object):
    def __init__(self, x, y, vx, vy, direction, sizex, sizey):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.direction = direction
        self.sizex = sizex
        self.sizey = sizey
        self.onGround = True

    def load_images(self, template_string, length):
        """
        Loads images of the form "L1.png" -> "L10.png".
        template string should equal somthing like "L%d.png".
        """
        image_list = [template_string % x for x in range(1, length+1)]
        loaded = []
        for image in image_list:
            loaded.append(pygame.image.load(image))
        return loaded

    def move(self):
        gameSize = pygame.display.get_surface().get_size()
        if self.y < gameSize[1] - self.sizey:
            self.onGround = False
        if self.y >= gameSize[1] - self.sizey:
            self.y = gameSize[1] - self.sizey
            self.onGround = True
        if not self.onGround:
            self.vy = 1
        self.x += self.vx
        self.y += self.vy

class Player(MovingObject):
    def __init__(self, win, x, y, vx=0, vy=0, direction=0):
        self.win = win
        self.left_list = super().load_images("L%d.png", 9)
        self.right_list = super().load_images("R%d.png", 9)
        sizex, sizey = self.left_list[0].get_rect().size
        super().__init__(x, y, vx, vy, direction, sizex, sizey)
        self.standing = pygame.image.load("standing.png")
        self.walkCount = 0
        self.onGround = False

    def draw(self):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if self.direction == 0:
            self.win.blit(self.standing, (self.x, self.y))
        if self.direction == -1:
            self.win.blit(self.left_list[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        if self.direction == 1:
            self.win.blit(self.right_list[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1

class Enemy(MovingObject):
    def __init__(self, win, x, y, vx, vy, direction):
        self.win = win
        self.left_list = super().load_images("L%dE.png", 11)
        self.right_list = super().load_images("R%dE.png", 11)
        sizex, sizey = self.left_list[0].get_rect().size

        super().__init__(x, y, vx, vy, direction, sizex, sizey)
        self.onGround = False


class Bullet(MovingObject):
    def __init__(self, win, x, y, vx, vy, direction):
        self.win = win
        super().__init__(x, y, vx, vy, direction)

def main():
    game = Game()
    # player = Player(0, 0)
    # player.load_images()

if __name__ == "__main__":
    main()