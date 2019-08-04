import numpy as np 
import pygame 
from pygame.locals import *

BLUE = (153, 204, 255)
RED = (255, 50, 50)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class NaughtsAndCrosses(object):
    def __init__(self, win, clock):
        self.win = win
        self.clock = clock
        self.board = np.zeros((3, 3))

        # self.board = np.random.choice([-1, 1], size=(3, 3))
        # self.board[1][1] = 0
        # self.board[1][0] = 0

        self.player_vs_player = True
        self.background = pygame.image.load("background.jpg")
        self.game_loop()

    def game_loop(self):
        playing = True
        while playing:
            self.clock.tick(30)
            self.draw_board()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == VIDEORESIZE:
                    self.win = pygame.display.set_mode(event.dict['size'], HWSURFACE|DOUBLEBUF|RESIZABLE)
                    self.win.blit(pygame.transform.scale(self.background, event.dict['size']), (0, 0))

            pygame.display.update()

    def draw_board(self):
        gameSize = pygame.display.get_surface().get_size()
        width = gameSize[0] // 100
        pygame.draw.line(self.win, WHITE, (gameSize[0] // 3, gameSize[1] // 10), (gameSize[0] // 3, 9*gameSize[1] // 10), width)
        pygame.draw.line(self.win, WHITE, (2 * gameSize[0] // 3, gameSize[1] // 10), (2 * gameSize[0] // 3, 9*gameSize[1] // 10), width)
        pygame.draw.line(self.win, WHITE, (gameSize[0] // 10, gameSize[1] // 3), (9 * gameSize[0] // 10, gameSize[1] // 3), width)
        pygame.draw.line(self.win, WHITE, (gameSize[0] // 10, 2 * gameSize[1] // 3), (9 * gameSize[0] // 10, 2 * gameSize[1] // 3), width)

        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 1:
                    centre = (int(1/6 * gameSize[0] + j * gameSize[0] // 3), int(1/6 * gameSize[1] + i * gameSize[1] // 3))
                    # draw X
                    pygame.draw.line(self.win, BLUE, centre, (centre[0] + width * 6, centre[1] + width * 6), int(width // 1.5))
                    pygame.draw.line(self.win, BLUE, centre, (centre[0] - width * 6, centre[1] - width * 6), int(width // 1.5))
                    pygame.draw.line(self.win, BLUE, centre, (centre[0] + width * 6, centre[1] - width * 6), int(width // 1.5))
                    pygame.draw.line(self.win, BLUE, centre, (centre[0] - width * 6, centre[1] + width * 6), int(width // 1.5))
                elif self.board[i][j] == -1:
                    # draw O
                    pygame.draw.circle(self.win, RED, (int(1/6 * gameSize[0] + j * gameSize[0] // 3), int(1/6 * gameSize[1] + i * gameSize[1] // 3)), width * 6, int(width // 1.5))
                


    def player_move(self):
        pass

    def computer_move(self, AI):
        pass

    def check_win(self):
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] == self.grid[i][j+1] and self.grid[i][j] == self.grid[i][j-1]:
                    # Horizontal line
                    return True
                elif self.grid[i][j] == self.grid[i+1][j] and self.grid[i][j] == self.grid[i-1][j]:
                    # Vertical Line
                    return True
                if i == 1 and j == 1:
                    # if in centre check diagonals
                    if self.grid[i][j] == self.grid[0][0] and self.grid[i][j] == self.grid[2][2]:
                        return True
                    elif self.grid[i][j] == self.grid[2][0] and self.grid[i][j] == self.grid[0][2]:
                        return True
        return False



class AI(object):
    def get_rand_ai_move(self, board):
        valid = False
        while not valid:
            rand_x = np.random.randint(3)
            rand_y = np.random.randint(3)
            if board[rand_x][rand_y] == 0:
                valid = True
        return (rand_x, rand_y)


def main():
    pygame.init()
    pygame.display.set_caption("Naughts and Crosses")
    clock = pygame.time.Clock()
    win = pygame.display.set_mode((500,500),HWSURFACE|DOUBLEBUF|RESIZABLE)
    game = NaughtsAndCrosses(win, clock)
    

if __name__ == "__main__":
    main()