import chess
import time

from ai import AI

class Game():

    def __init__(self, game_mode, delay=None):
        self.board = chess.Board()
        self.white_next = True
        self.game_mode = game_mode
        self.delay = delay
        self.white = AI() \
            if game_mode in ['auto', 'white-auto'] else None
        self.black = AI() \
            if game_mode in ['auto', 'black-auto'] else None   

    def play(self, move_name=None):
        if move_name is None:
            if self.white_next:
                move = self.white.choose_move(self.board)   # White AI
            else:
                move = self.black.choose_move(self.board)   # Black AI
            self.playMove(move)
        else:                                               # Manual
            move = chess.Move.from_uci(move_name)
            self.playMove(move)

        if (self.white_next and self.white is not None) \
                or (not self.white_next and self.black is not None):  # Next is AI
            if self.delay is not None: time.sleep(self.delay)
            self.play()

    def playMove(self, move):  # FIXME: Catch Exceptions
        if not move in self.board.legal_moves:
            raise Exception("Dumbass, that shit ain't legal")

        self.board.push(move)

        # Check if game is over
        if self.board.is_checkmate():
            if self.white_next:
                raise Exception("White won boooiiiii!!")
            else:
                raise Exception("Black won boooiiiii!!")
        elif self.board.is_insufficient_material() or self.board.is_stalemate():  # draw
            raise Exception("issa draw bish...")
        elif self.board.is_game_over():
            raise Exception("The game ended for some reason...")
        else:
            self.white_next = not self.white_next


if __name__ == '__main__':

    game = Game('Manual')
    mate_sequence = ['e2e4', 'e7e5', 'd1h5', 'e8e7', 'h5e5']
    white_sequence = mate_sequence[::2]
    black_sequence = mate_sequence[1::2]

    for move in mate_sequence:
        game.play(move)



