from PySide2.QtCore import QAbstractTableModel
from PySide2.QtCore import Qt
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

class MinesweeperModel(QAbstractTableModel):
    def __init__(self, parent = None):
        super(MinesweeperModel, self).__init__(parent)
        self._data = []
        self.visitedZeros = []
        self.newGame()

    def newGame(self):
        mines = [HIDE, MINE] * MINE_COUNT
        rest = [HIDE, 0] * (COLUMN_COUNT * ROW_COUNT - MINE_COUNT)
        self._data = np.concatenate((mines, rest), axis=0)
        np.random.shuffle(self._data)
        self._data = self._data.reshape((ROW_COUNT, COLUMN_COUNT, 2))
        
        for x in range(self.rowCount()):
            for y in range(self.columnCount()):
                if self._data[x][y][1] is MINE:
                    self.calculateAdjacent(x, y)
        
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
            self._data[a][b][1] += 1 

    def findAllZeros(self, x, y):
        for a, b in self.findAdjacent(x, y):
            if self._data[a][b][1] == 0 and (a, b) not in self.visitedZeros:
                index = self.index(a, b)
                self.setData(index, DISPLAY)
                self.visitedZeros.append((a, b))
                self.findAllZeros(a, b)

    def setAsFlaged(self, x, y):
        index = self.index(x, y)
        self.setData(index, FLAG)

    def setAsClicked(self, x, y):
        index = self.index(x, y)
        self.setData(index, DISPLAY)
    
    def rowCount(self, parent = None):
        return len(self._data)

    def columnCount(self, parent = None):
        return len(self._data[0])

    def setData(self, index, value, role= None):
        self._data[index.row()][index.column()][0] = value
        self.dataChanged.emit(index, index)

    def data(self, index, role = None):
        return self._data[index.row()][index.column()]

if __name__ == "__main__":
    a = MinesweeperModel()
    a.newGame()