from game import Game

MODE = 'Semi-auto' # 'Manual' 'Semi-auto' 'Auto'

if MODE == 'Auto':
    # TODO
    pass

elif MODE == 'Manual' or 'Semi-auto':

    from GUI import MainWindow
    from PyQt5.QtWidgets import QApplication

    if MODE == 'Semi-auto':
        game = Game(True)
    else:
        game = Game(False)

    app = QApplication([])
    window = MainWindow(game)
    window.show()
    app.exec()

else:
    raise Exception('Invalid game mode')


