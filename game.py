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

    def change_mode(self, game_mode):
        self.game_mode = game_mode
        self.board.reset()
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
        else:
            move = chess.Move.from_uci(move_name)
        
        result = self.playMove(move)       
        if result is not None: return result

        # Next is AI
        if (self.white_next and self.white is not None) or (not self.white_next and self.black is not None):
            if self.delay is not None: time.sleep(self.delay)
            return self.play()

    def playMove(self, move):  # FIXME: Catch Exceptions
        if not move in self.board.legal_moves:
            raise Exception("Dumbass, that shit ain't legal")
        else:
            self.board.push(move)

        # Check if game is over
        if self.board.is_checkmate():
            if self.white_next:
                return 1
            else:
                return 2
        elif self.board.is_insufficient_material() or self.board.is_stalemate():  # draw
            return 3
        elif self.board.is_game_over():
            return 4
        else:
            self.white_next = not self.white_next
            return None

if __name__ == '__main__':

    game = Game('Manual')
    mate_sequence = ['e2e4', 'e7e5', 'd1h5', 'e8e7', 'h5e5']
    white_sequence = mate_sequence[::2]
    black_sequence = mate_sequence[1::2]

    for move in mate_sequence:
        game.play(move)



