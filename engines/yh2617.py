from __future__ import absolute_import
from engines import Engine
from copy import deepcopy

class StudentEngine(Engine):
    # Set the infinity
    INFINITY = float('inf')
    WEIGHTS = [4, -3, 2, 2, 2, 2, -3, 4,
               -3, -4, -1, -1, -1, -1, -4, -3,
               2, -1, 1, 0, 0, 1, -1, 2,
               2, -1, 0, 1, 1, 0, -1, 2,
               2, -1, 0, 1, 1, 0, -1, 2,
               2, -1, 1, 0, 0, 1, -1, 2,
               -3, -4, -1, -1, -1, -1, -4, -3,
               4, -3, 2, 2, 2, 2, -3, 4]
    num_node = 0
    num_dup = 0
    node_list = []
    branch_list = [0, 0, 0]
    ply_maxmin = 4
    ply_alpha = 4

    """ Game engine that implements a simple fitness function maximizing the
    difference in number of pieces in the given color's favor. """
    def __init__(self):
        self.alpha_beta = False

    def get_move(self, board, color, move_num=None,
                 time_remaining=None, time_opponent=None):
        """ Return a move for the given color that maximizes the difference in 
        number of pieces for that color. """
        if self.alpha_beta == False:
            score, finalmove = self._minmax(board, color, move_num, time_remaining, time_opponent, StudentEngine.ply_maxmin)
        else:
            score, finalmove = self._minmax_with_alpha_beta(board, color, move_num, time_remaining, time_opponent, StudentEngine.ply_alpha)
        return finalmove

    def _minmax(self, board, color, move_num, time_remaining, time_opponent, ply):
        moves = board.get_legal_moves(color)
        if move_num > 7 and move_num < 15:
            StudentEngine.ply_maxmin = 2
        if time_remaining < 20:
            return (0, max(moves, key=lambda move: self.greedy(board, color, move)))
        if not isinstance(moves, list):
            score = self.heuristic(board, color)
            return score, None
        return_move = moves[0]
        bestscore = -StudentEngine.INFINITY
        for move in moves:
            newboard = deepcopy(board)
            newboard.execute_move(move, color)
            score = self.min_score(newboard, -color, move_num, ply-1)
            if score > bestscore:
                bestscore = score
                return_move = move
        return bestscore, return_move

    def max_score(self, board, color, move_num, ply):
        moves = board.get_legal_moves(color)
        if ply == 0:
            return self.heuristic(board, color)
        bestscore = -StudentEngine.INFINITY
        for move in moves:
            newboard = deepcopy(board)
            newboard.execute_move(move, color)
            score = self.min_score(newboard, -color, move_num, ply-1)
            if score > bestscore:
                bestscore = score
        return bestscore

    def min_score(self, board, color, move_num, ply):
        moves = board.get_legal_moves(color)
        if ply == 0:
            return self.heuristic(board, color)
        bestscore = StudentEngine.INFINITY
        for move in moves:
            newboard = deepcopy(board)
            newboard.execute_move(move, color)
            score = self.max_score(newboard, -color, move_num, ply-1)
            if score < bestscore:
                bestscore = score
        return bestscore

    def _minmax_with_alpha_beta(self, board, color, move_num, time_remaining, time_opponent, ply):
        moves = board.get_legal_moves(color)
        if not isinstance(moves, list):
            score = board.count(color)
            return score, None
        return_move = moves[0]
        bestscore = -StudentEngine.INFINITY
        if time_remaining < 5:
            return 0, max(moves, key=lambda move: self.greedy(board, color, move))
        for move in moves:
            newboard = deepcopy(board)
            newboard.execute_move(move, color)
            StudentEngine.branch_list[0] += 1
            score = self.min_score_alpha_beta(newboard, -color, move_num, ply-1, -StudentEngine.INFINITY, StudentEngine.INFINITY)
            if score > bestscore:
                bestscore = score
                return_move = move
        return bestscore, return_move

    def max_score_alpha_beta(self, board, color, move_num, ply, alpha, beta):
        if ply == 0:
            return self.heuristic(board, color)
        bestscore = -StudentEngine.INFINITY
        for move in board.get_legal_moves(color):
            newboard = deepcopy(board)
            newboard.execute_move(move, color)
            score = self.min_score_alpha_beta(newboard, -color, move_num, ply - 1, alpha, beta)
            if score > bestscore:
                bestscore = score
            if bestscore >= beta:
                return bestscore
            alpha = max(alpha, bestscore)
        return bestscore

    def min_score_alpha_beta(self, board, color, move_num, ply, alpha, beta):
        if ply == 0:
            return self.heuristic(board, color)
        bestscore = StudentEngine.INFINITY
        for move in board.get_legal_moves(color):
            newboard = deepcopy(board)
            newboard.execute_move(move, color)
            score = self.max_score_alpha_beta(newboard, -color, move_num, ply - 1, alpha, beta)
            if score < bestscore:
                bestscore = score
            if bestscore <= alpha:
                return bestscore
            beta = min(beta, bestscore)
        return bestscore

    def heuristic(self, board, color):
        return 2 * self.cornerweight(color, board) + 3 * self._get_cost(board, color)

    def cornerweight(self, color, board):
        total = 0
        for i in range(64):
            if board[i // 8][i % 8] == color:
                total += StudentEngine.WEIGHTS[i]
            if board[i // 8][i % 8] == -color:
                total -= StudentEngine.WEIGHTS[i]
        return total

    def greedy(self, board, color, move):
        """ Return the difference in number of pieces after the given move 
        is executed. """
        newboard = deepcopy(board)
        newboard.execute_move(move, color)
        num_pieces_op = len(newboard.get_squares(color*-1))
        num_pieces_me = len(newboard.get_squares(color))
        return num_pieces_me - num_pieces_op

    def _get_cost(self, board, color):
        """ Return the difference in number of pieces after the given move 
        is executed. """
        num_pieces_op = board.count(-color)
        num_pieces_me = board.count(color)
        return num_pieces_me - num_pieces_op

engine = StudentEngine
