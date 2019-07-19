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
        # while -1 * np.sum(self.grid) < n_mines:
        #     empty = False
        #     while not empty:
        #         x, y = np.random.choice(self.N, size=2)
        #         if self.grid[x][y] == 0:
        #             empty = True
        #     self.grid[x][y] = -1
        # while -1 * np.sum(self.grid) > n_mines:
        #     mine = False
        #     while not mine:
        #          x, y = np.random.choice(self.N, size=2)
        #          if self.grid[x][y] == 1:
        #              mine = True
        #     self.grid[x][y] = 0


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
            self.selection_grid[i][j] = -2
            self.bomb_hit(i, j)
            return 0
        if self.grid[i][j] == 0:
            # No bombs
            zeros = True
            x = i
            y = j
            while zeros:
                self.reveal_empty_neighbours(i, j)
        else:
            self.grid[i][j] = self.selection_grid[i][j]

    def reveal_empty_neighbours(self, i, j):
        start_x = i-1
        end_x = i + 1
        start_y = j - 1
        end_y = j + 1
        if i == 0:
            start_x = i
        if i == self.N - 1:
            end_x = i
        if j == 0:
            start_x = j
        if j == self.N - 1:
            end_x = j

        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                if x == i and y == j:
                    continue
                if self.grid[x][y] == 0: #  and self.selection_grid[x][y] != self.grid[x][y]:  # May need this
                    self.selection_grid[x][y] = self.grid[x][y]
                    self.reveal_empty_neighbours(x, y)

    def flag_added(self, i, j):
        # Flag values set to 9 as this is greatr than all possible values.
        # (in a 2d grid).
        if not self.selection_grid[i][j]:
            # If cell is empty add a flag
            self.selection_grid[i][j] = 9
        if self.selection_grid[i][j] == 9:
            # If already flagged.
            self.selection_grid[i][j] = 0
            # Set back to original unflaged value of 0.

    def bomb_hit(self, i, j):
        for i in range(self.N):
            for j in range(self.N):
                if self.grid[i][j] == -1:
                    self.selection_grid[i][j] = -1
        self._show_grid()

    def select_point(self):
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

    def run_game(self):
        running = True
        while running:
            pygame.time.delay(100)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            self.draw_grid()
            pygame.display.update()


    def draw_grid(self):
        n_boxes = self.grid.N
        buffer = 5
        box_width = (self.width-buffer/2) // n_boxes
        for i in range(n_boxes):
            for j in range(n_boxes):
                pygame.draw.rect(self.win, (200, 200, 200), ((i * box_width) + buffer, (j * box_width) + buffer, box_width - buffer, box_width - buffer))


def main(argv):
    argv = [10, 10]
    if len(argv) != 2:
        print("python MineSweeper.py N n_mines")
        sys.exit()
    grid = Grid(int(argv[0]), int(argv[1]))
    game = Game(grid)
    # grid._show_grid()
    # grid.select_point()
    


if __name__ == '__main__':
    main(sys.argv[1:])
