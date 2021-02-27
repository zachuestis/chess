import chess
import chess.svg

class Game():

    def __init__(self):
        self.board = chess.Board()
        self.white_next = True

    def play_white(self, move_name):
        move = chess.Move.from_uci(move_name)

        if not self.white_next:
            raise Exception("Bruh it's not your turn")

        if not move in self.board.legal_moves:
            raise Exception("Dumbass, that shit ain't legal")

        self.board.push(move)
        self.white_next = False
        self.end_move()

    def play_black(self, move_name):
        move = chess.Move.from_uci(move_name)

        if self.white_next:
            raise Exception("Bruh it's not your turn")

        if not move in self.board.legal_moves:
            raise Exception("Dumbass, that shit ain't legal")

        self.board.push(move)
        self.white_next = True
        self.end_move()

    def end_move(self):

        suff = self.board.is_insufficient_material()
        stale = self.board.is_stalemate()

        if self.board.is_checkmate():
            print("You won boooiiiii!!")
            return False
        elif suff or stale:  # draw
            print("issa draw bish...")
        elif self.board.is_game_over():
            raise Exception("The game ended for some reason...")
        else:
            return True


if __name__ == '__main__':

    game = Game()
    mate_sequence = ['e2e4', 'e7e5', 'd1h5', 'e8e7', 'h5e5']

    for move in mate_sequence:
        if game.white_next:
            game.play_white(move)
        else:
            game.play_black(move)

