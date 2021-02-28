import chess
import chess.svg

from ai import AI

class Game():

    def __init__(self, black_auto):
        self.board = chess.Board()
        self.white_next = True
        self.black_auto = black_auto
        self.ai = AI()

    def play(self, move_name):
        if self.white_next:
            self.play_white(move_name)
        else:
            self.play_black(move_name)

    def play_white(self, move_name):
        move = chess.Move.from_uci(move_name)

        if not self.white_next:
            raise Exception("Bruh it's not your turn")

        if not move in self.board.legal_moves:
            raise Exception("Dumbass, that shit ain't legal")

        self.board.push(move)
        self.white_next = False
        self.end_move()

        if self.black_auto:
            self.play_black('auto')

    def play_black(self, move_name):

        if move_name == 'auto':
            move = self.ai.choose_move(self.board.legal_moves)
        else:
            move = chess.Move.from_uci(move_name)

        if self.white_next:
            raise Exception("Bruh it's not your turn")

        if not move in self.board.legal_moves:
            raise Exception("Dumbass, that shit ain't legal")

        self.board.push(move)
        self.white_next = True
        self.end_move()

    def end_move(self):
        if self.board.is_checkmate():
            print("You won boooiiiii!!")
            return False
        elif self.board.is_insufficient_material() or self.board.is_stalemate():  # draw
            print("issa draw bish...")
        elif self.board.is_game_over():
            raise Exception("The game ended for some reason...")
        else:
            return True


if __name__ == '__main__':

    game = Game(False) 
    mate_sequence = ['e2e4', 'e7e5', 'd1h5', 'e8e7', 'h5e5']
    white_sequence = mate_sequence[::2]
    black_sequence = mate_sequence[1::2]

    for move in mate_sequence:
        if game.white_next:
            game.play_white(move)
        else:
            game.play_black(move)
 import pygame
 import pygame.freetype
 from pygame.sprite import Sprite    
 from pygame.rect import Rect

  BLUE = (106, 159, 181)
  WHITE = (255, 255, 255)


  def create_surface_with_text (text, font_size, text_rgb, bg_rgb):
      font = pygame.freetype.Sysfont("Courier", font_size, bold=True)
      surface, _ = font.render (text = text, fgcolor=text_rgb, bgcolor=bg_rgb)
      return surface.convert_alpha


class UIElements(Sprite):
    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb):

        



