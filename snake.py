import numpy as np
import pygame

class Snake:
    def __init__(self, width, height, walls=False):
        self.grid_size = np.array([20, 20])
        self.window_size = np.array([width, height])
        self.speed = 1
        self.body_arr = [[0, 0], [0, 1], [0, 2], [0, 3]]
        self.padding = 5
        self.size = self.window_size / self.grid_size
        self.direction = 1 # 0 = N, 1 = E, 2 = S, 3 = W
        self.food_loc = [np.random.randint(self.grid_size[0]), np.random.randint(self.grid_size[1])]
        self.food_eaten = 0
        self.walls = walls

    def grid_to_pixel(self, pos):
        x_pos = (pos[0] / self.grid_size[0]) * self.window_size[0]
        y_pos = (pos[1] / self.grid_size[1]) * self.window_size[1]
        return [x_pos, y_pos]

    def draw(self, win):
        head = True
        for section in self.body_arr:
            col = (255, 255, 255)
            if head:
                col = (255, 0, 0)
                head = False
            pos = self.grid_to_pixel(section)
            pygame.draw.rect(win, col, (pos[0] + self.padding, pos[1] + self.padding, self.size[0] - self.padding, self.size[1] - self.padding))

        food_pos = self.grid_to_pixel(self.food_loc)
        col = (0, 255, 0)
        pygame.draw.rect(win, col, (food_pos[0] + self.padding, food_pos[1] + self.padding, self.size[0] - self.padding, self.size[1] - self.padding))

    def move(self):
        next_position = np.zeros((len(self.body_arr), 2))
        if self.direction == 0:
            next_position[0][0] = self.body_arr[0][0]
            next_position[0][1] = (self.body_arr[0][1] - 1) % self.grid_size[1]
        if self.direction == 1:
            next_position[0][0] = (self.body_arr[0][0] + 1) % self.grid_size[0]
            next_position[0][1] = self.body_arr[0][1] 
        if self.direction == 2:
            next_position[0][0] = self.body_arr[0][0]
            next_position[0][1] = (self.body_arr[0][1] + 1) % self.grid_size[1]
        if self.direction == 3:
            next_position[0][0] = (self.body_arr[0][0] - 1) % self.grid_size[0]
            next_position[0][1] = self.body_arr[0][1] 

        next_position[1:] = self.body_arr[0: -1]
        self.body_arr = next_position

    def collisions(self):
        if self.body_arr[0][0] == self.food_loc[0] and self.body_arr[0][1] == self.food_loc[1]:
            new_body = np.zeros((len(self.body_arr) + 1, 2))
            new_body[:-1] = self.body_arr
            new_body[-1] = self.body_arr[1]
            self.body_arr = new_body
            self.new_food()
            self.food_eaten += 1
            if self.food_eaten % 5 == 0:
                return 2

        for position in self.body_arr[1:]:
            if position[0] == self.body_arr[0][0] and position[1] == self.body_arr[0][1]:
                return 1

        if self.walls:
            if np.abs(self.body_arr[0][0] - self.body_arr[1][0]) >= 2 or np.abs(self.body_arr[0][1] - self.body_arr[1][1]) >= 2:
                return 1
        return 0

    def new_food(self):
        self.food_loc = [np.random.randint(self.grid_size[0]), np.random.randint(self.grid_size[1])]
 

class Game:
    def __init__(self, win):
        self.win = win
        self.gameSize = [600, 600]

    def welcomeScreen(self):
        waiting = True
        walls = True
        s = Snake(self.gameSize[0], self.gameSize[1], False)
        count = 0
        while waiting:
            pygame.time.delay(50)
            self.win.fill((0, 0, 0))


            wall_col = (0, 200, 0)
            if not walls:
                wall_col = (200, 0, 0)
            pygame.time.delay(100)
            font = pygame.font.Font('freesansbold.ttf', 32) 
            go_text = font.render("Welcome to Snake!"  , True, (0, 255, 0))
            cont_text = font.render("Press space bar to continue.", True, (0, 255, 0))
            font = pygame.font.Font('freesansbold.ttf', 24) 
            if walls:
                wall_val = "On"
            else:
                wall_val = "Off"
            wall_text = font.render("Walls [%s] (w)" % wall_val, True, wall_col)
            go_textRect = go_text.get_rect()  
            cont_textRect = cont_text.get_rect()
            wall_textRect = wall_text.get_rect()
            go_textRect.center = (self.gameSize[0] // 2, self.gameSize[1] // 2) 
            cont_textRect.center = (self.gameSize[0] // 2, 6.5 * self.gameSize[1] // 8)
            wall_textRect.center = (self.gameSize[0] // 2, 7.5 * self.gameSize[1] // 8)

            self.win.blit(go_text, go_textRect)
            self.win.blit(cont_text, cont_textRect)
            self.win.blit(wall_text, wall_textRect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    return walls
                if keys[pygame.K_w]:
                    if walls:
                        walls = False
                    else:
                        walls = True
            if count >= np.random.randint(3, 7):
                while True:
                    val = np.random.randint(4)
                    if val != (s.direction + 2) % 4:
                        s.direction = val
                        break
                count = 0 
            s.move()
            s.collisions()
            s.draw(self.win)
            pygame.display.update()
            count += 1
        return 0

    def runGame(self, walls=True):
        s = Snake(self.gameSize[0], self.gameSize[1], walls)
        run = True
        speed = 200
        while(run):
            pygame.time.delay(speed)
            self.win.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    exit()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                    s.direction = 0
                if keys[pygame.K_RIGHT]:
                    s.direction = 1
                if keys[pygame.K_DOWN]:
                    s.direction = 2
                if keys[pygame.K_LEFT]:
                    s.direction = 3
            s.draw(self.win)
            s.move()
            ret = s.collisions()
            if(ret == 1):
                return len(s.body_arr)
            if ret == 2 and speed >= 25:
                speed -= 20
            pygame.display.update()
        pygame.quit()
        exit()
        return 0

    def gameOver(self, length):
        print("Game Over!")
        print("Final length of: %d" % length)
        paused = True
        walls = True
        while paused:
            wall_col = (0, 200, 0)
            if not walls:
                wall_col = (200, 0, 0)
            pygame.time.delay(100)
            font = pygame.font.Font('freesansbold.ttf', 32) 
            go_text = font.render("GAME OVER!", True, (0, 255, 0))
            cont_text = font.render("Press space bar to continue.", True, (0, 255, 0))
            font = pygame.font.Font('freesansbold.ttf', 24) 
            if walls:
                wall_val = "On"
            else:
                wall_val = "Off"
            wall_text = font.render("Walls [%s] (w)" % wall_val, True, wall_col)
            go_textRect = go_text.get_rect()  
            cont_textRect = cont_text.get_rect()
            wall_textRect = wall_text.get_rect()
            go_textRect.center = (self.gameSize[0] // 2, self.gameSize[1] // 2) 
            cont_textRect.center = (self.gameSize[0] // 2, 6.5 * self.gameSize[1] // 8)
            wall_textRect.center = (self.gameSize[0] // 2, 7.5 * self.gameSize[1] // 8)

            self.win.blit(go_text, go_textRect)
            self.win.blit(cont_text, cont_textRect)
            self.win.blit(wall_text, wall_textRect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    self.runGame(walls = walls)
                if keys[pygame.K_w]:
                    if walls:
                        walls = False
                    else:
                        walls = True
                pygame.display.update()


def main():
    pygame.init()
    pygame.display.set_caption("Snake")
    win = pygame.display.set_mode((600, 600))
    run = True
    game = Game(win)
    walls = game.welcomeScreen()
    while(run):
        length = game.runGame(walls = walls)
        game.gameOver(length)


if __name__ == "__main__":
    main()
