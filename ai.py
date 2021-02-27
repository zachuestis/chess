import random


class AI :

    def choose_move(self, legal_moves):
        moves = [move for move in legal_moves]
        return random.choice(moves)