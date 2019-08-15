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

        self.player_vs_player = False
        self.players_turn = False
        self.naughts = True

        self.background = pygame.image.load("background.jpg")
        self.win.blit(pygame.transform.scale(self.background, pygame.display.get_surface().get_size()), (0, 0))

    def game_loop(self):
        playing = True
        while playing:
            self.clock.tick(10)
            self.draw_board()
            grid_x = None
            grid_y = None

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == VIDEORESIZE:
                    self.win = pygame.display.set_mode(event.dict['size'], HWSURFACE|DOUBLEBUF|RESIZABLE)
                    self.win.blit(pygame.transform.scale(self.background, event.dict['size']), (0, 0))

            # Needs to be here to prevent the computer making a mover after the game has been won.
            if not self.players_turn:
                grid_x, grid_y = self.computer_move()

            click1, click2, click3 = pygame.mouse.get_pressed()
            if click1 and self.players_turn:
                mx, my = pygame.mouse.get_pos()
                gameSize = pygame.display.get_surface().get_size()
                grid_x = mx // (gameSize[0] // 3)
                grid_y = my // (gameSize[1] // 3)
                if self.board[grid_y][grid_x] == 0:
                    self.player_move(grid_x, grid_y)

            if self.check_win():
                # Check if game winner
                if self.naughts:
                    winner = "Crosses"
                else:
                    winner = "Naughts"
                playing = False
            if self.check_stalemate():
                winner = "No one :("
                playing = False

            pygame.display.update()
            
        new_game = self.show_end_game_page(winner)
        return new_game

    def show_end_game_page(self, winner):
        game_over = True
        gameSize = pygame.display.get_surface().get_size()

        while game_over:
            self.clock.tick(10)
            gameSize = pygame.display.get_surface().get_size()
        
            self.draw_board()
            font = pygame.font.Font('freesansbold.ttf', 32) 
            text = font.render("Winner: %s" % winner, True, BLACK, False) 
            textRect = text.get_rect()  
            textRect.center = (gameSize[0] // 2, gameSize[1] // 2) 
            self.win.blit(text, textRect) 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == VIDEORESIZE:
                    self.win = pygame.display.set_mode(event.dict['size'], HWSURFACE|DOUBLEBUF|RESIZABLE)
                    self.win.blit(pygame.transform.scale(self.background, event.dict['size']), (0, 0))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                return True
            elif keys[pygame.K_n]:
                return False
            pygame.display.update()
        return False

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
                


    def player_move(self, x, y):
        if self.naughts:
            self.board[y][x] = -1
            self.naughts = False
        else:
            self.board[y][x] = 1
            self.naughts = True

        if not self.player_vs_player:
            self.players_turn = False


    def computer_move(self):
        obj = AI()
        if self.naughts:
            turn = -1
        else:
            turn = 1
        vals = obj.move(self.board, turn, level=2)
        if self.naughts:
            self.board[vals[0]][vals[1]] = -1
            self.naughts = False
        else:
            self.board[vals[0]][vals[1]] = 1
            self.naughts = True
        self.players_turn = True
        return vals

    def check_win(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    continue
                if i == 1 and j == 1:
                    if self.board[0][0] == self.board[1][1] and self.board[2][2] == self.board[1][1] and self.board[1][1] != 0:
                        return True
                    if self.board[2][0] == self.board[1][1] and self.board[0][2] == self.board[1][1] and self.board[1][1] != 0:
                        return True
                elif self.board[i][j] == self.board[(i+1)%3][j] and self.board[i][j] == self.board[(i-1)%3][j]:
                    return True
                if self.board[i][j] == self.board[i][(j+1)%3] and self.board[i][j] == self.board[i][(j-1)%3]:
                    return True       
        return False

    def check_stalemate(self):
        count = np.count_nonzero(self.board==0)
        if count == 0:
            return True
        else:
            return False


class AI(object):
    def move(self, board, turn, level=1):
        if level == 1:
            return self.get_rand_ai_move(board)

        elif level == 2:
            return self.get_winning_ai_move(board, turn)

        elif level == 3:
            return self.play_best_strat(board, turn)

    def get_rand_ai_move(self, board):
        valid = False
        while not valid:
            rand_x = np.random.randint(3)
            rand_y = np.random.randint(3)
            if board[rand_x][rand_y] == 0:
                valid = True
        return (rand_x, rand_y)

    def get_winning_ai_move(self, board, turn):
        # check for a winning move
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = turn
                    if self.check_win(board):
                        board[i][j] = 0
                        return (i, j)
                    else:
                        board[i][j] = 0
        # if no winning moves then check to block a win
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = turn * -1
                    if self.check_win(board):
                        board[i][j] = 0
                        return (i, j)
                    else:
                        board[i][j] = 0
        # If no winnig or blocking then pick random
        return self.get_rand_ai_move(board)


    def play_best_strat(self, board, turn):
        # if the board is empty pick a corner
        if np.sum(board) == 0 or (board[1][1] != 0 and np.abs(np.sum(board)) == 1):
            return (np.random.choice([0, 2]), np.random.choice([0, 2]))    
        if board[1][1] != 0:
            return (1, 1)              

    def check_win(self, board):
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    continue
                if i == 1 and j == 1:
                    if board[0][0] == board[1][1] and board[2][2] == board[1][1] and board[1][1] != 0:
                        return True
                    if board[2][0] == board[1][1] and board[0][2] == board[1][1] and board[1][1] != 0:
                        return True
                elif board[i][j] == board[(i+1)%3][j] and board[i][j] == board[(i-1)%3][j]:
                    return True
                if board[i][j] == board[i][(j+1)%3] and board[i][j] == board[i][(j-1)%3]:
                    return True       
        return False


def main():
    pygame.init()
    pygame.display.set_caption("Naughts and Crosses")
    clock = pygame.time.Clock()
    game = True
    while game:
        win = pygame.display.set_mode((500,500),HWSURFACE|DOUBLEBUF|RESIZABLE)
        game = NaughtsAndCrosses(win, clock)
        game = game.game_loop()
    

if __name__ == "__main__":
    main()