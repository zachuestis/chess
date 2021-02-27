import chess

class Player:

    def __init__(self, color):
        self.white = color


class Game:

    def __init__(self):
        self.board = chess.Board()
        self.white_next = True
        self.white = Player(True)
        self.black = Player(False)

    def play_white(self, move_name):
        move = chess.Move.from_uci(move_name)

        if not self.white_next:
            raise Exception("Bruh it's not your turn")

        self.board.push(move)
        self.white_next = False

    def play_black(self):
        pass