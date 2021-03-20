import random

class AI():

    def __init__(self, board):
        self.board = board

    def choose_move(self):
        # Currently chooses random legal move
        moves = [move for move in self.board.legal_moves]
        return random.choice(moves)
        

