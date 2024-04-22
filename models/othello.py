from config.config import PLAYER, CPU, EMPTY_SPACE
from models.game import Game


class Othello(Game):
    """Create a new Othello game.
    
        Atributtes:
            cost_table (list): It contains the cost of every single cell of the board.
            width (int): The width of the board
            height (int): The height of the board
    """
    def __init__(self):
        self.cost_table = [
            [100, -20, 10,  5,  5, 10, -20, 100],
            [-20, -50, -2, -2, -2, -2, -50, -20],
            [ 10, -2,  -1, -1, -1, -1,  -2,  10],
            [  5, -2,  -1, -1, -1, -1,  -2,   5],
            [  5, -2,  -1, -1, -1, -1,  -2,   5],
            [ 10, -2,  -1, -1, -1, -1,  -2,  10],
            [-20, -50, -2, -2, -2, -2, -50, -20],
            [100, -20, 10,  5,  5, 10, -20, 100]
        ]
        self.width = len(self.cost_table)
        self.height = self.width
 
    def actions(self, state, player):
        """Return a list of the allowable moves at this point"""
        moves = []
        if player == PLAYER:
            oponent = CPU
        else:
            oponent = PLAYER
        # get player's chips positions
        player_positions = []
        for row in range(0, self.width):
            for col in range(0, self.height):
                if state[row][col] == player:
                    player_positions.append((row, col))
        for pos in player_positions:
            row = pos[0]
            col = pos[1]
            # horizontal movements
            if row + 2 < self.width:
                if state[row + 1][col] == oponent:
                    if state[row + 2][col] == EMPTY_SPACE:
                        state_copy = self._copy_state(state)
                        state_copy[row + 1][col] = player
                        state_copy[row + 2][col] = player
                        moves.append(state_copy)
            if row - 2 >= 0:
                if state[row - 1][col] == oponent:
                    if state[row - 2][col] == EMPTY_SPACE:
                        state_copy = self._copy_state(state)
                        state_copy[row - 1][col] = player
                        state_copy[row - 2][col] = player
                        moves.append(state_copy)
            # vertical movements
            if col + 2 < self.height:
                if state[row][col + 1] == oponent:
                    if state[row][col + 2] == EMPTY_SPACE:
                        state_copy = self._copy_state(state)
                        state_copy[row][col + 1] = player
                        state_copy[row][col + 2] = player
                        moves.append(state_copy)
            if col - 2 < self.height:
                if state[row][col - 1] == oponent:
                    if state[row][col - 2] == EMPTY_SPACE:
                        state_copy = self._copy_state(state)
                        state_copy[row][col - 1] = player
                        state_copy[row][col - 2] = player
                        moves.append(state_copy)
            # diagonal movements
            # upper right diagonal
            if row + 2 < self.width and col - 2 >= 0:
                if state[row + 1][col - 1] == oponent:
                    if state[row + 2][col - 2] == EMPTY_SPACE:
                        state_copy = self._copy_state(state)
                        state_copy[row + 1][col - 1] = player
                        state_copy[row + 2][col - 2] = player
                        moves.append(state_copy)
            # upper left diagonal
            if row - 2 >= 0 and col - 2 >= 0:
                if state[row - 1][col - 1] == oponent:
                    if state[row - 2][col - 2] == EMPTY_SPACE:
                        state_copy = self._copy_state(state)
                        state_copy[row - 1][col - 1] = player
                        state_copy[row - 2][col - 2] = player
                        moves.append(state_copy)
            # lower right diagonal
            if row + 2 < self.width and col + 2 < self.height:
                if state[row + 1][col + 1] == oponent:
                    if state[row + 2][col + 2] == EMPTY_SPACE:
                        state_copy = self._copy_state(state)
                        state_copy[row + 1][col + 1] = player
                        state_copy[row + 2][col + 2] = player
                        moves.append(state_copy)
            # lower left diagonal
            if row - 2 >= 0 and col + 2 < self.height:
                if state[row - 1][col + 1] == oponent:
                    if state[row - 2][col + 2] == EMPTY_SPACE:
                        state_copy = self._copy_state(state)
                        state_copy[row - 1][col + 1] = player
                        state_copy[row - 2][col + 2] = player
                        moves.append(state_copy)
        return moves

    def _copy_state(self, state):
        # returns a copy of a certain state
        state_copy = []
        for row in state:
            row_copy = []
            for value in row:
                row_copy.append(value)
            state_copy.append(row_copy)
        return state_copy

    def utility(self, state, player):
        """Return the value of this final state to player."""
        if player == PLAYER:
            oponent = CPU
        else:
            oponent = PLAYER
        player_sum = 0
        oponent_sum = 0
        for row in range(0, self.width):
            for col in range(0, self.height):
                if state[row][col] == player:
                    player_sum = player_sum + self.cost_table[row][col]
                elif state[row][col] == oponent:
                    oponent_sum = oponent_sum + self.cost_table[row][col]
        return player_sum - oponent_sum

    def terminal_state(self, state):
        """Return True if this is a final state for the game."""
        return False
