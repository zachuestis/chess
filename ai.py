import random


class AI:

    def choose_move(self, board):
        # Currently chooses random legal move
        moves = [move for move in board.legal_moves]
        return random.choice(moves)