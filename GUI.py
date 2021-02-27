import chess
import chess.svg

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QWidget


class MainWindow(QWidget):

    def __init__(self, game):
        super().__init__()

        self.setWindowTitle("Zachy's Chess")
        self.setGeometry(300, 300, 700, 700)

        self.widgetSvg = QSvgWidget(parent=self)
        self.svgX = 50                          # top left x-pos of chessboard
        self.svgY = 50                          # top left y-pos of chessboard
        self.cbSize = 600                       # size of chessboard
        self.widgetSvg.setGeometry(
            self.svgX, self.svgY, self.cbSize, self.cbSize)
        self.coordinates = True

        self.margin = 0.05*self.cbSize if self.coordinates == True else 0
        self.squareSize = (self.cbSize - 2 * self.margin) / 8.0

        self.game = game
        self.chessboard = game.board
        self.selectedPiece = None
        self.pieceToMove = [None, None]

    @pyqtSlot(QWidget)
    def mousePressEvent(self, event):
        if self.svgX < event.x() <= self.svgX + self.cbSize and self.svgY < event.y() <= self.svgY + self.cbSize:   # mouse on chessboard
            if event.buttons() == Qt.LeftButton:
                # if the click is on chessBoard only
                if self.svgX + self.margin < event.x() < self.svgX + self.cbSize - self.margin and self.svgY + self.margin < event.y() < self.svgY + self.cbSize - self.margin:
                    file = int(
                        (event.x() - (self.svgX + self.margin))/self.squareSize)
                    rank = 7 - \
                        int((event.y() - (self.svgY + self.margin))/self.squareSize)
                    # chess.sqare.mirror() if white is on top
                    square = chess.square(file, rank)
                    piece = self.chessboard.piece_at(square)
                    coordinates = '{}{}'.format(chr(file + 97), str(rank + 1))

                    self.selectedPiece = None
                    if self.pieceToMove[0] is not None:
                        self.makeMove(coordinates)
                        piece = None
                        coordinates = None

                    elif piece is not None:
                        if piece.color == self.game.white_next:  # True if both white or both black
                            self.selectedPiece = square

                    self.pieceToMove = [piece, coordinates]
                else:
                    print('coordinates clicked')
                # Envoke the paint event.
                self.update()
        else:
            QWidget.mousePressEvent(self, event)

    @pyqtSlot(QWidget)
    def paintEvent(self, event):
        self.chessboardSvg = chess.svg.board(
            self.chessboard, size=self.cbSize, coordinates=self.coordinates, check=self.selectedPiece).encode("UTF-8")
        self.widgetSvg.load(self.chessboardSvg)

    def makeMove(self, coordinates):
        # TODO: Show invalid move, winning, etc.
        try:
            self.game.play(self.pieceToMove[1] + coordinates)
        except Exception as e:
            print(e)
        

if __name__ == '__main__':

    import game
    game = game.Game(False)

    app = QApplication([])
    window = MainWindow(game)
    window.show()
    app.exec()
