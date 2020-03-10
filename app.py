import sys
from PyQt5.QtWidgets import QApplication
from Game import TicTacToe

if __name__ == '__main__':
    app = QApplication(sys.argv)
    tictactoe = TicTacToe()
    sys.exit(app.exec_())