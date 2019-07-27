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
        enemy = Enemy(self.win, self.size[0] * 4// 6, 50)
        objects.append(player)
        objects.append(enemy)
        while running:
            self.clock.tick(27)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                player.direction = 1
                player.vx = 2
            if keys[pygame.K_LEFT]:
                player.direction = -1
                player.vx = -2
            if keys[pygame.K_UP]:
                if player.onGround:
                    player.vy = -10
            if keys[pygame.K_DOWN]:
                player.vy = 5
                if player.onGround:
                    player.direction = 0
                    player.vx = 0
            if keys[pygame.K_SPACE]:
                objects.append(player.shoot())
            for i, obj in enumerate(objects):  # Remove players and objects when they are of the screen
                if not obj.onScreenCheck():
                    objects.pop(i)

            self.draw(objects)

    def draw(self, objects):
        self.win.blit(self.background, (0,0))
        # print("Length of objects: " + str(len(objects)))
        for obj in objects:
            obj.draw()
            obj.move()
        pygame.display.update()
        
        
class MovingObject(object):
    def __init__(self, x, y, vx, vy, direction, sizex, sizey, catagory=None):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.direction = direction
        self.sizex = sizex
        self.sizey = sizey
        self.onGround = True
        self.onDisplay = True
        self.catagory = catagory

    def onScreenCheck(self):
        if not self.onDisplay:
            return False
        gameSize = pygame.display.get_surface().get_size()
        if self.x > gameSize[0] or self.x <  - self.sizex:
            return False
        if self.y > gameSize[1] + self.sizey or self.y < 0:
            return False
        return True

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

    def move(self, groundBuffer=10):
        # print("%s position: %d, %d" % (self.catagory, self.x, self.y))
        if self.catagory == "Enemy" and self.x <= 1:
            self.onDisplay = False
        gameSize = pygame.display.get_surface().get_size()
        if self.y < gameSize[1] - self.sizey - groundBuffer:
            self.onGround = False
        if self.y >= gameSize[1] - self.sizey - groundBuffer:
            self.y = gameSize[1] - self.sizey - groundBuffer
            self.onGround = True
        if not self.onGround:
            self.vy += 1
        if self.x >= gameSize[0] - self.sizex:
            self.vx = 0
            self.x -= 1
            self.direction = 0  ## Maybe get rid of
        if self.x <= 0:
            self.vx = 0
            self.x += 1
            self.direction = 0 ## maybe get rid of
        self.x += self.vx
        self.y += self.vy

class Player(MovingObject):
    def __init__(self, win, x, y, vx=0, vy=0, direction=0):
        self.win = win
        self.left_list = super().load_images("L%d.png", 9)
        self.right_list = super().load_images("R%d.png", 9)
        sizex, sizey = self.left_list[0].get_rect().size
        super().__init__(x, y, vx, vy, direction, sizex, sizey, "Player")
        self.standing = pygame.image.load("standing.png")
        self.walkCount = 0
        self.onGround = False

    def shoot(self):
        bullet = Bullet(self.win,  self.x, self.y, self.vx + 3, 0, self.direction)
        return bullet

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
    def __init__(self, win, x, y, vx=-1, vy=0, direction=-1):
        self.win = win
        self.left_list = super().load_images("L%dE.png", 11)
        self.right_list = super().load_images("R%dE.png", 11)
        sizex, sizey = self.left_list[0].get_rect().size

        super().__init__(x, y, vx, vy, direction, sizex, sizey, "Enemy")
        self.onGround = False
        self.walkCount = 0

    def draw(self):
        if self.walkCount + 1 >= 30:
            self.walkCount = 0
        if self.direction == -1:
            self.win.blit(self.left_list[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        if self.direction == 1:
            self.win.blit(self.right_list[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1


class Bullet(MovingObject):
    def __init__(self, win, x, y, vx, vy, direction):
        self.win = win
        super().__init__(x, y, vx, vy, direction, 1, 1, catagory="Bullet")

    def draw(self):
        pygame.draw.circle(self.win, (0, 0, 0), (int(self.x), int(self.y)), 10, 1)

def main():
    game = Game()
    # player = Player(0, 0)
    # player.load_images()

if __name__ == "__main__":
    main()