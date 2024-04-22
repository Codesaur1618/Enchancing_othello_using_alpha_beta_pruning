from config.config import PLAYER, CPU

class AlphaBeta():
    """Implment the alpha-beta algorithm.

        Atributtes:
            game (Game): The game where the algorithm will be used on.
            depth (int): Maximum depth.
    """
    def __init__(self, game, depth):
        self.game = game
        self.depth = depth

    def alpha_beta_search(self, state):
        """The alpha-beta algorithm.

            Atributtes:
                state (list): Actual state of the game.
            
            Returns:
                The best move for the machine. 
        """
        infinity = float("inf")
        alpha = -infinity
        beta = infinity
        best_value = -infinity
        best_state = None
        player = CPU
        for action in self.game.actions(state, player):
            value = self.__max_value(state, alpha, beta, 0)
            if value > best_value:
                best_value = value
                best_state = action
        return best_state

    def __max_value(self, state, alpha, beta, level):
        player = CPU
        if self.game.terminal_state(state) or level > self.depth:
            return self.game.utility(state, player)
        infinity = float('inf')
        value = -infinity
        for action in self.game.actions(state, player):
            value = max(value, self.__min_value(action, alpha, beta, level + 1))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    def __min_value(self, state, alpha, beta, level):    
        player = PLAYER
        if self.game.terminal_state(state) or level > self.depth:
            return self.game.utility(state, player)
        infinity = float('inf')
        value = -infinity
        for action in self.game.actions(state, player):
            value = max(value, self.__max_value(action, alpha, beta, level + 1))
            if value <= alpha:
                return value
            beta = max(beta, value)
        return value
