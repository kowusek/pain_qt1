from PySide2.QtCore import QAbstractTableModel, QObject
from PySide2.QtCore import Qt, Signal
import numpy as np

ROW_COUNT = 8
COLUMN_COUNT = 8
MINE_COUNT = 10

# item -> [display: int, value: int]

#display:
DISPLAY = 1
HIDE = 0
FLAG = -1

#value:
MINE = -1

class GameWon(QObject):
    signal = Signal()

class GameOver(QObject):
    signal = Signal()

class UpdateFlagCount(QObject):
    signal = Signal(int)

gameWon = GameWon()
gameOver = GameOver()
updateFlagCount = UpdateFlagCount()

class MinesweeperModel(QAbstractTableModel):
    def __init__(self, parent = None):
        super(MinesweeperModel, self).__init__(parent)
        self._data = []
        self.clicked = set()
        self.flagCount = 10
        self.newGame()

    def newGame(self):
        self.beginResetModel()

        self.clicked = set()
        self.flagCount = 10

        mines = [[HIDE, MINE]] * MINE_COUNT
        rest = [[HIDE, 0]] * (COLUMN_COUNT * ROW_COUNT - MINE_COUNT)
        self._data = np.concatenate((mines, rest), axis=0)
        np.random.shuffle(self._data)
        self._data = self._data.reshape((ROW_COUNT, COLUMN_COUNT, 2))
        
        for x in range(self.rowCount()):
            for y in range(self.columnCount()):
                index = self.index(x, y)
                if index.data()[1] == MINE:
                    self.calculateAdjacent(x, y)

        self.endResetModel()
        
    def isInBounds(self, x, y):
        if x < self.rowCount() and x >= 0 and y < self.columnCount() and y >= 0:
            return True
        return False

    def findAdjacent(self, x, y):
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if self.isInBounds(x + dx, y + dy) and (dx != 0 or dy != 0):
                    yield x + dx, y + dy

    def calculateAdjacent(self, x: int, y: int):
        for a, b in self.findAdjacent(x, y):
            index = self.index(a, b)
            if index.data()[1] != MINE:
                index.data()[1] += 1

    def findAllZeros(self, x, y):
        for a, b in self.findAdjacent(x, y):
            index = self.index(a, b)
            if index.data()[1] == 0:
                if index not in self.clicked:
                    self.setData(index, DISPLAY)
                    self.clicked.add(index)
                    self.findAllZeros(a, b)
            else:
                self.clicked.add(index)
                self.setData(index, DISPLAY)

    def setAsFlaged(self, x, y):
        if self.flagCount > 0:
            index = self.index(x, y)
            self.setData(index, FLAG)
            self.flagCount -= 1
            updateFlagCount.signal.emit(self.flagCount)

    def setAsClicked(self, x, y):
        index = self.index(x, y)
        self.setData(index, DISPLAY)
        if index.data()[1] == 0:
            self.findAllZeros(x, y)
        elif index.data()[1] == MINE:
            gameOver.signal.emit()
        self.clicked.add(index)
        self.checkIfWon()
    
    def checkIfWon(self):
        if len(self.clicked) == COLUMN_COUNT * ROW_COUNT - MINE_COUNT:
            gameWon.signal.emit()

    def rowCount(self, parent = None):
        return len(self._data)

    def columnCount(self, parent = None):
        return len(self._data[0])

    def setData(self, index, value, role = None):
        try:
            if self._data[index.row()][index.column()][0] == FLAG:
                self.flagCount += 1
                updateFlagCount.signal.emit(self.flagCount)
            self._data[index.row()][index.column()][0] = value
            self.dataChanged.emit(index, index)
        except:
            return False
        return True

    def data(self, index, role = None):
        return self._data[index.row()][index.column()]

if __name__ == "__main__":
    model = MinesweeperModel()
    model.newGame()