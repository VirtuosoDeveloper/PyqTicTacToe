import collections
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QPushButton, QDialog, QLabel, QLineEdit, QWidget, QAction, QDesktopWidget

# TODO-P: Maybe add color for symbol. Alt: Use stylesheets.
Player = collections.namedtuple('Player', ['name', 'symbol'])


class TicTacToe(QMainWindow):

    def __init__(self):
        super().__init__()
        self.xPlayer = Player('X Player', 'X')
        self.oPlayer = Player('O Player', 'O')
        self.currentPlayer = self.xPlayer
        self.turnIndicator = f"{self.currentPlayer.name}'s Turn"
        self.initUI()

    def initUI(self):
        self.board = TicTacToeBoard(self)
        self.setCentralWidget(self.board)
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
        gameMenu = self.menuBar().addMenu('Game')
        gameMenu.addAction(self.resetAction())
        settingsMenu = self.menuBar().addMenu('Settings')
        settingsMenu.addAction(self.setNameAction())
        settingsMenu.addAction(self.turnIndicatorToggle())

    def resetAction(self):
        action = QAction('Reset', self)
        action.setShortcut('Ctrl+R')
        action.setToolTip('Reset Game')
        action.triggered.connect(self.reset)
        return action
    
    def reset(self):
        self.board.reset()
        self.currentPlayer = self.xPlayer
        self.updateIndicator()

    def updateIndicator(self):
        # TODO-Q: Does PyQt have parameter binding? Can I also use signals / slots to 'auto-update' variables / displayed text?
        self.turnIndicator = f"{self.currentPlayer.name}'s Turn"
        self.statusBar.showMessage(self.turnIndicator)

    def setNameAction(self):
        action = QAction('Set Name(s)', self)
        action.setShortcut('Ctrl+A')
        action.setStatusTip('Set Player Name(s)')
        action.triggered.connect(self.setNameDialog)
        return action

    def setNameDialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('Set Player Name(s)')
        dialog.resize(600, 200)
        layout = QGridLayout()
        xText = QLineEdit()
        oText = QLineEdit()
        layout.addWidget(QLabel(f'<b>{self.xPlayer.name}:</b>'), 0, 0)
        layout.addWidget(xText, 0, 1)
        layout.addWidget(QLabel(f'<b>{self.oPlayer.name}:</b>'), 1, 0)
        layout.addWidget(oText, 1, 1)
        dialog.setLayout(layout)
        enterButton = QPushButton('Enter')
        enterButton.clicked.connect(lambda: self.setName(xText.text(), oText.text()))
        enterButton.clicked.connect(dialog.accept)
        layout.addWidget(enterButton, 2, 0)
        dialog.exec_()

    def setName(self, xName, oName):
        if xName:
            self.xPlayer = self.xPlayer._replace(name=xName)
        if oName:
            self.oPlayer = self.oPlayer._replace(name=oName)
        self.currentPlayer = self.xPlayer if self.currentPlayer is self.xPlayer else self.oPlayer
        self.updateIndicator()

    def buttonClicked(self):
        button = self.sender()
        button.capture(self.currentPlayer.symbol)
        self.togglePlayer()

    def togglePlayer(self):
        self.currentPlayer = self.oPlayer if self.currentPlayer is self.xPlayer else self.xPlayer
        self.updateIndicator()

    def turnIndicatorToggle(self):
        action = QAction('Turn Indicator', self, checkable=True)
        action.setShortcut('Ctrl+T')
        action.setChecked(True)
        action.setStatusTip('Toggle Status Indicator')
        action.triggered.connect(self.toggleTurnIndicator)
        return action
    
    def toggleTurnIndicator(self, state):
        if state:
            self.statusBar.show()
            self.statusBar.showMessage(self.turnIndicator)
        else:
            self.statusBar.hide()

    def showVictory(self):
        winner = self.oPlayer if self.currentPlayer is self.xPlayer else self.xPlayer
        self.statusBar.showMessage(f'{winner.name} wins!')

    def center(self):
        qr = self.frameGeometry()
        qr.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(qr.topLeft())


class TicTacToeBoard(QWidget):  

    def __init__(self, parent):
        super().__init__(parent)
        self.game = parent
        layout = QGridLayout()
        self.setLayout(layout)
        self.grid = [[TicTacToeCell() for i in range(3)] for j in range(3)]
        positions = [(i, j) for i in range(3) for j in range(3)]
        for position in positions:
            x, y = position
            button = self.grid[x][y]
            button.clicked.connect(parent.buttonClicked)
            button.clicked.connect(self.evaluateBoard)
            layout.addWidget(button, *position)
    
    def reset(self):    
        for row in self.grid:
            for cell in row:
                cell.reset()
    
    def disable(self):
        for row in self.grid:
            for cell in row:
                cell.setEnabled(False)
    
    def evaluateBoard(self):
        self.evaluateCells(self.grid[0][0], self.grid[1][1], self.grid[2][2])
        self.evaluateCells(self.grid[0][2], self.grid[1][1], self.grid[2][0])
        for i in range(3):
            self.evaluateCells(self.grid[i][0], self.grid[i][1], self.grid[i][2])
            self.evaluateCells(self.grid[0][i], self.grid[1][i], self.grid[2][i])

    def evaluateCells(self, a, b, c):
        if a.captured() and a.text is b.text is c.text:
            self.disable()
            self.game.showVictory()


class TicTacToeCell(QPushButton):

    def __init__(self):
        super().__init__()
        self.setMinimumSize(400, 400)
        self.text = ''
    
    def captured(self):
        return self.text

    def capture(self, symbol):
        self.text = symbol
        self.setText(symbol)
        self.setEnabled(False)

    def reset(self):
        self.text = ''
        self.setText(self.text)
        self.setEnabled(True)
    
    def __repr__(self):
        return f'[{self.text}]'