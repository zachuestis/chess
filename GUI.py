import chess
import chess.svg

from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QComboBox 
from PyQt5.QtGui import QFont

GAME_MODES = ['Play White', 'Play Black', 'Two Player', 'Auto']
_GAME_MODES = ['black-auto', 'white-auto', 'manual', 'auto']


class MainWindow(QWidget):
    move_signal = pyqtSignal()

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

        # Chess game
        self.game = game
        self.chessboard = game.board
        self.game_mode = _GAME_MODES[0]
        self.selectedPiece = None
        self.pieceToMove = [None, None]
        self.next_move = None
        self.move_signal.connect(self.newMove)

        # Starting Screen
        self.starting_screen()
        self.playing = False

    def starting_screen(self):
        self.chessboardSvg = chess.svg.board(self.chessboard, size=self.cbSize).encode("UTF-8")
        self.widgetSvg.load(self.chessboardSvg)

        self.startBtn = QPushButton('Start', self)
        self.startBtn.resize(self.startBtn.sizeHint())
        self.startBtn.clicked.connect(self.startButtonEvent)

        self.modeSelector = QComboBox()
        self.modeSelector.addItems(GAME_MODES)
        self.modeSelector.currentIndexChanged.connect(self.modeChange)

        self.vbox = QVBoxLayout()
        self.vbox.setContentsMargins(295, 260, 295, 260)
        self.vbox.addWidget(self.modeSelector)
        self.vbox.addWidget(self.startBtn)
        self.setLayout(self.vbox)

    def modeChange(self, idx):
        self.game_mode = _GAME_MODES[idx]

    def startButtonEvent(self, event):
        self.startBtn.hide()
        self.modeSelector.hide()
        self.playing = True
        self.game.change_mode(self.game_mode)

        if self.game_mode in ["auto", "white-auto"]:
            self.move_signal.emit()
        
        self.update()

    def newMove(self):
        # TODO: Show invalid move, winning, etc.
        # FIXME: Auto does not visualize every move...
        try:
            self.game.play(self.next_move)
        except Exception as e:
            print(e)

        self.update()
        
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
                    if self.game_mode == "white-auto": # if white is on top
                        file = 7 - file
                        rank = 7 - rank
                    square = chess.square(file, rank)
                    piece = self.chessboard.piece_at(square)
                    coordinates = '{}{}'.format(chr(file + 97), str(rank + 1))

                    self.selectedPiece = None
                    if self.pieceToMove[0] is not None:
                        self.next_move = self.pieceToMove[1] + coordinates
                        self.move_signal.emit()
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
        if not self.playing: return
        flipped = True if self.game_mode == 'white-auto' else False
        self.chessboardSvg = chess.svg.board(
            self.chessboard, size=self.cbSize, coordinates=self.coordinates, check=self.selectedPiece, flipped=flipped).encode("UTF-8")
        self.widgetSvg.load(self.chessboardSvg)

if __name__ == '__main__':

    import game
    game = game.Game(False)

    app = QApplication([])
    window = MainWindow(game)
    window.show()
    app.exec()



