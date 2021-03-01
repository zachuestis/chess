import chess
import chess.svg

from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QComboBox, QLabel
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
        self.vbox = QVBoxLayout()
        self.vbox.setContentsMargins(295, 300, 295, 300)
        self.setLayout(self.vbox)
        self.starting_screen()

    def starting_screen(self):
        self.startBtn = QPushButton('Start', self)
        self.startBtn.resize(self.startBtn.sizeHint())
        self.startBtn.clicked.connect(self.startButtonEvent)

        self.modeSelector = QComboBox()
        self.modeSelector.addItems(GAME_MODES)
        self.modeSelector.currentIndexChanged.connect(self.modeChange)

        self.vbox.addWidget(self.modeSelector)
        self.vbox.addWidget(self.startBtn)

    def modeChange(self, idx): 
        # FIXME: Sometimes selection gets stuck after auto game
        self.game_mode = _GAME_MODES[idx]

    def startButtonEvent(self, event):
        self.startBtn.hide()
        self.modeSelector.hide()
        self.game.change_mode(self.game_mode)
        self.update()
        if self.game_mode in ["auto", "white-auto"]: self.move_signal.emit()

    def gameOver(self, message):
        self.result = QLabel(message)
        self.result.resize(self.result.sizeHint())
        self.result.setStyleSheet("background-color:white; border-radius:5px") # FIXME: Overflows, center text
        self.replayBtn = QPushButton('Replay', self)
        self.replayBtn.resize(self.replayBtn.sizeHint())
        self.replayBtn.clicked.connect(self.retryButtonEvent)

        self.vbox.addWidget(self.result)
        self.vbox.addWidget(self.replayBtn)

    def retryButtonEvent(self):
        self.result.hide()
        self.replayBtn.hide()
        self.next_move = None
        self.game_mode = _GAME_MODES[0]
        self.starting_screen()

    def newMove(self):
        # TODO: Show invalid move, etc.
        # FIXME: Auto does not visualize every move...
        try:
            result = self.game.play(self.next_move)
            self.update()
        
            if result == 1: # white wins
                self.gameOver("White won boooiiiii!!")
            elif result == 2: # black wins
                self.gameOver("Black won boooiiiii!!")
            elif result == 3: # draw
                self.gameOver("issa draw bish...")
            elif result == 4: # game over
                self.gameOver("Game Over")

        except Exception as e:
            print(e)
        
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
        flipped = True if self.game_mode == 'white-auto' else False
        self.chessboardSvg = chess.svg.board(
            self.chessboard, size=self.cbSize, coordinates=self.coordinates, 
            check=self.selectedPiece, flipped=flipped).encode("UTF-8")
        self.widgetSvg.load(self.chessboardSvg)

if __name__ == '__main__':

    import game
    game = game.Game(False)

    app = QApplication([])
    window = MainWindow(game)
    window.show()
    app.exec()



