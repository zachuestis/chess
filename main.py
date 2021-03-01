from game import Game

MODE = 'white-auto'
GUI = True

game = Game(MODE, delay=None)

if GUI:
    from GUI import MainWindow
    from PyQt5.QtWidgets import QApplication

    app = QApplication([])
    window = MainWindow(game)
    window.show()
    app.exec()

elif MODE == 'auto':
    try:
        game.play()
    except Exception as e:
        print(e)
    
else:
    raise Exception("Invalid Mode")


