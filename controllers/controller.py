from models.alpha_beta import AlphaBeta
from views.board import Board
from config.config import PLAYER, CPU, EMPTY_SPACE, INITIAL_STATE, NUM_COLS, NUM_ROWS
from models.othello import Othello

from tkinter import Tk


class Controller:
    """Create a controller that's in charge of the board's behaviour.

        Atributtes:
            state (list): The actual state of the game. It's a representation of the board.
            board (Board): The board. This controller is in charge of it.
            waiting_movement (bool): Is the game waiting for the player to move?
            initial_pos (tuple): The initial position for every user move.
            player (int): Representation of the current player.
            possible_moves (list): All the possible moves user can make from initial_pos.
            positions_to_take (dict): Contains all the positions that user will take.

        Args:
            view (Board): The board of the game.
    """
    def __init__(self):
        self.state = INITIAL_STATE
        root = Tk(className="Othello!")
        self.view = Board(root, self)
        self.game = Othello()
        self.waiting_movement = False
        self.initial_pos = (-1,-1)
        self.player = PLAYER
        self.possible_moves = []
        self.positions_to_take = {}
        self.__clear_positions_to_take()
        root.mainloop()

    def __clear_positions_to_take(self):
        self.positions_to_take = {
            "01": [],
            "10": [],
            "11": [],
            "0-1": [],
            "-10": [],
            "-1-1": [],
            "-11": [],
            "1-1": []
        }

    def touch_board(self, event):
        """It's called every time the player clicks on the board.

            Atributtes:
                evnt (tkinter.Event): contains the coordinates where the user has clicked
        """
        row = int((event.x / self.view.cellwidth))
        col = int((event.y / self.view.cellheight))
        
        if row < 0 or row >= NUM_ROWS or col < 0 or col >= NUM_COLS:
            raise Exception
        if self.player == PLAYER:
            if self.state[row][col] == PLAYER:
                if not self.waiting_movement:
                    self.initial_pos = (row,col)
                    self.__where_can_i_move()
                    self.view.draw_possible_moves(self.possible_moves)
                    self.view.draw_chip(PLAYER, row, col, True)
                    self.waiting_movement = True
            if self.state[row][col] == EMPTY_SPACE and self.waiting_movement:
                final_pos = (row, col)
                if self.__try_to_move(final_pos):
                    self.view.draw_grid()
                    self.player = CPU
            if self.state[row][col] == CPU or self.state[row][col] == PLAYER:
                if self.waiting_movement and self.initial_pos != (row,col):
                    self.waiting_movement = False
        else:
            alpha_beta = AlphaBeta(self.game, 3)
            cpu_action = alpha_beta.alpha_beta_search(self.state)
            if cpu_action is None:
                # the machine doesn't know what to do!
                self.__player_won()
            else:
                self.state = cpu_action
            self.player = PLAYER
        if not self.waiting_movement:
            self.view.draw_chips(self.state)

    def __where_can_i_move(self):
        # find all the possbile moves that user can make from initial_pos
        self.possible_moves = []
        self.__clear_positions_to_take()

        for x_dir in range(-1, 2):
            for y_dir in range(-1, 2):
                if x_dir == 0 and y_dir == 0:
                    continue
                dir = (x_dir, y_dir)
                self.__possible_moves(dir)
        
    def __possible_moves(self, dir):
        # find all the possible moves from 'initial_pos' given a direction 'dir'
        key = str(dir[0]) + str(dir[1])
        found_an_empty_space = False
        out_of_board = False
        found_enemy = False

        x = self.initial_pos[0]
        y = self.initial_pos[1]
        while not found_an_empty_space and not out_of_board:
            x += dir[0]
            y += dir[1]
            if x == NUM_COLS or x < 0 or y == NUM_ROWS or y < 0:
                # we are out of the board!
                out_of_board = True
                continue
            if self.state[x][y] == self.player:
                # we found a friend!
                break
            if self.state[x][y] == CPU:
                found_enemy = True
                self.positions_to_take.get(key).append((x, y))
            elif self.state[x][y] == EMPTY_SPACE:
                found_an_empty_space = True
                if found_enemy:
                    self.possible_moves.append((x, y))
                    self.positions_to_take.get(key).append((x, y))
                continue

    def __try_to_move(self, final_pos):
        """ Find out whether it's possible for the player to move to a certain pos or not.
            In case this is true, it makes the move.

            Returns: 
                True if it's possible to move.
        """
        if final_pos in self.possible_moves: # it's possible to move
            # find the direction
            for _, positions in self.positions_to_take.items(): 
                if final_pos in positions:
                    # take the positions
                    for pos in positions:
                        x = pos[0]
                        y = pos[1]
                        self.state[x][y] = self.player
                    break
            return True
        return False

    def __player_won(self):
        self.view.show_player_victory()

    def start_game(self):
        self.view.draw_grid()
        self.view.draw_chips(self.state)

    def give_up(self):
        self.game_over()

    def game_over(self):
        exit()
