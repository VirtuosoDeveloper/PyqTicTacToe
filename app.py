import sys
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QPushButton, QInputDialog, QWidget, QAction, QApplication, QDesktopWidget

class TicTacToe(QMainWindow):

    def __init__(self):
        super().__init__()
        self.xPlayer = 'X Player'
        self.yPlayer = 'Y Player'
        self.currentPlayer = self.xPlayer
        self.turnIndicator = f"{self.currentPlayer}'s Turn"
        self.initUI()

    def initUI(self):
        self.setCentralWidget(TicTacToeBoard())
        self.initElements()
        self.setWindowTitle('Tic Tac Toe')
        self.resize(1200, 1200)
        self.center()
        self.show()

    def initElements(self):
        self.initStatusBar()
        self.initMenu()

    def initStatusBar(self):
        self.statusBar = self.statusBar()
        self.statusBar.showMessage(self.turnIndicator)

    def initMenu(self):
        settingsMenu = self.menuBar().addMenu('Settings')
        settingsMenu.addAction(self.setNameAction())
        settingsMenu.addAction(self.TurnIndicatorToggle())

    def setNameAction(self):
        action = QAction('Set Name(s)', self)
        action.setShortcut('Ctrl+A')
        action.setStatusTip('Set Player Name(s)')
        # TODO: action.triggered.connect(self.setNameDialog)
        return action

    def togglePlayer(self):
        if self.currentPlayer is self.xPlayer:
            self.currentPlayer = self.yPlayer
        else:
            self.currentPlayer = self.xPlayer

    def TurnIndicatorToggle(self):
        action = QAction('Turn Indicator', self, checkable=True)
        action.setShortcut('Ctrl+T')
        action.setChecked(True)
        action.setStatusTip('Toggle Turn Indicator')
        action.triggered.connect(self.toggleTurnIndicator)
        return action

    
    def toggleTurnIndicator(self, state):
        if state:
            self.statusBar.show()
            self.statusBar.showMessage(self.turnIndicator)
        else:
            self.statusBar.hide()

    def center(self):
        qr = self.frameGeometry()
        qr.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(qr.topLeft())

class TicTacToeBoard(QWidget):  

    def __init__(self):
        super().__init__()
        grid = QGridLayout()
        self.setLayout(grid)
        positions = [(i, j) for i in range(3) for j in range(3)]
        for position in positions:
            button = QPushButton('')
            button.setMinimumSize(400, 400)
            grid.addWidget(button, *position)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    tictactoe = TicTacToe()
    sys.exit(app.exec_())