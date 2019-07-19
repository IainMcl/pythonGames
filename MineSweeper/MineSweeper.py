import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.signal import convolve2d
import sys
import pygame

class Grid:
    def __init__(self, N, n_mines):
        self.N = N
        self.n_mines = n_mines
        ps = [1-(n_mines/N**2), n_mines/N**2]
        self.grid = np.random.choice([0, -1], size=(N, N), p=ps)
        self.init_grid()
        self.selection_grid = np.ones((N, N)) * 10
        # self.selection_grid = self.grid

    def init_grid(self):
        nn = np.array([[-1, -1, -1],
                       [-1,  0, -1],
                       [-1, -1, -1]])
        grid = convolve2d(self.grid, nn, mode='same', boundary='fill')
        for i in range(self.N):
            for j in range(self.N):
                if self.grid[i][j] == -1:
                    grid[i][j] = -1
        self.grid = grid.copy()

    def _show_grid(self):
        plt.imshow(self.grid)
        plt.colorbar()
        plt.show()

    def cell_clicked(self, i, j):
        # val = self.grid[i][j]
        if self.grid[i][j] == -1:
            # bomb hit
            # self.selection_grid[i][j] = -2
            self.bomb_hit(i, j)
            return 1
        elif self.grid[i][j] == 0:
            # No bombs
            zeros = True # unused
            x = i
            y = j
            self.selection_grid[i][j] = 0
            self.reveal_empty_neighbours(i, j)
        else:
            self.selection_grid[i][j] = self.grid[i][j]
        return 0

    def reveal_empty_neighbours(self, i, j):
        for x in range(i -1, i + 2):
            for y in range(j - 1, j + 2):
                if x < 0 or x >= self.N or y < 0 or y >= self.N or (x == i and y == j):
                    continue
                if self.grid[x][y] == 0 and self.selection_grid[x][y] != 0:
                    self.selection_grid[x][y] = self.grid[x][y]
                    self.reveal_empty_neighbours(x, y)
                else:
                    self.selection_grid[x][y] = self.grid[x][y]
                

    def flag_added(self, i, j):
        # print("Flag added: %d, %d" % (i, j))
        # Flag values set to 9 as this is greatr than all possible values.
        # (in a 2d grid).
        if self.selection_grid[i][j] == 10:
            # If cell is empty add a flag
            self.selection_grid[i][j] = 9
        elif self.selection_grid[i][j] == 9:
            # If already flagged.
            self.selection_grid[i][j] = 10
            # Set back to original unflaged value of 10.

    def bomb_hit(self, i, j):
        for i in range(self.N):
            for j in range(self.N):
                if self.grid[i][j] == -1:
                    self.selection_grid[i][j] = -1
        # self._show_grid()

    def reset(self):
        for i in range(self.N):
            for j in range(self.N):
                if self.grid[i][j] == -1:
                    self.selection_grid[i][j] = 10

    def select_point(self):
        """ Not used """
        a = input("Enter the grid location:").split(" ")
        a = list(map(int, a))
        self.cell_clicked(a[0], a[1])

class Game:
    def __init__(self, grid):
        self.grid = grid
        pygame.init()
        self.width = 600
        self.win = pygame.display.set_mode((self.width, self.width))
        pygame.display.set_caption("MineSweeper")
        self.run_game() ## Needs removed once a ome page has been made
        self.flag = pygame.image.load("red_flag.png") # Still haveing issues
        if self.flag:
            print("HERE")
        else:
            print("THERE")
        # self.win.blit(self.flag, (0,0))

    def get_grid_pos(self, mx, my):
        """ Takes the mouse position in pixels and translates in to grid position. """
        n_boxes = self.grid.N
        buffer = 5
        box_width = (self.width-buffer/2) // n_boxes
        grid_x = int(mx // box_width)
        grid_y = int(my // box_width)
        # print(grid_x, grid_y)
        return grid_x, grid_y

    def run_game(self):
        running = True
        while running:
            pygame.time.delay(150)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            keys = pygame.key.get_pressed()
            click1, click2, click3 = pygame.mouse.get_pressed()
            if click1:
                mx, my = pygame.mouse.get_pos()
                grid_x, grid_y = self.get_grid_pos(mx, my)
                if(self.grid.cell_clicked(grid_x, grid_y)):
                    self.end_game()
            if click3:
                mx, my = pygame.mouse.get_pos()
                grid_x, grid_y = self.get_grid_pos(mx, my)
                self.grid.flag_added(grid_x, grid_y)
            if keys[pygame.K_r]:
                self.grid.reset()

            self.draw_grid()
            pygame.display.update()


    def draw_grid(self):
        n_boxes = self.grid.N
        buffer = 3
        box_width = (self.width-buffer/2) // n_boxes
        font = pygame.font.Font('freesansbold.ttf', 30)
        for i in range(n_boxes):
            for j in range(n_boxes):
                # print(self.grid.selection_grid[i][j])
                val = str(int(self.grid.selection_grid[i][j]))
                if val == "10" or val == "0":
                    val = ""
                if val == "-1":
                    val = "!"
                if val == "9":
                    val = "/>"
                box_col = (170, 170, 170)
                col = (0, 0, 0)
                if self.grid.selection_grid[i][j] == 10: # or self.grid.selection_grid[i][j] == 9:
                    box_col = (200, 200, 200)
                elif self.grid.selection_grid[i][j] == 0:
                    box_col = (0, 150, 0)
                elif self.grid.selection_grid[i][j] == 1:
                    col = (20, 150, 0)
                elif self.grid.selection_grid[i][j] == 2:
                    col = (40, 120, 0)
                elif self.grid.selection_grid[i][j] == 3:
                    col = (60, 100, 0)
                elif self.grid.selection_grid[i][j] == 4:
                    col = (80, 80, 0)
                elif self.grid.selection_grid[i][j] == 5:
                    col = (100, 60, 0)
                elif self.grid.selection_grid[i][j] == 6:
                    col = (120, 40, 0)
                elif self.grid.selection_grid[i][j] == 7:
                    col = (140, 20, 0)
                elif self.grid.selection_grid[i][j] == 8:
                    col = (150, 0, 0)
                elif self.grid.selection_grid[i][j] == 9:
                    box_col = (0, 50, 255)
                elif self.grid.selection_grid[i][j] == -1:
                    box_col = (200, 0, 0)
                
                pygame.draw.rect(self.win, box_col, ((i * box_width) + buffer, (j * box_width) + buffer, box_width-buffer, box_width-buffer))
                text = font.render("%s" % val, True, col)
                textRect = text.get_rect()
                textRect.center = ((i * box_width) + buffer + box_width // 2, (j * box_width) + buffer + box_width // 2)
                
                self.win.blit(text, textRect)
                # self.win.blit(self.flag, (0,0))
    
    def end_game(self):
        print("GAME OVER")



def main(argv):
    argv = [10, 20]
    if len(argv) != 2:
        print("python MineSweeper.py N n_mines")
        sys.exit()
    grid = Grid(int(argv[0]), int(argv[1]))
    game = Game(grid)
    

if __name__ == '__main__':
    main(sys.argv[1:])
