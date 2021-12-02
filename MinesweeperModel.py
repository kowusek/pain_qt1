from PySide2.QtCore import QAbstractTableModel
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
    def __init__(self):
        super(MinesweeperModel, self).__init__()
        self._data = []
        self.populateData()

    def populateData(self):
        mines = [HIDE, MINE] * MINE_COUNT
        rest = [HIDE, 0] * (COLUMN_COUNT * ROW_COUNT - MINE_COUNT)
        self._data = np.concatenate((mines, rest), axis=0)
        np.random.shuffle(self._data)
        self._data = self._data.reshape((ROW_COUNT, COLUMN_COUNT, 2))
        
        for x in range(self.rowCount()):
            for y in range(self.columnCount()):
                if self._data[x][y][1] is MINE:
                    self.calculateAdjacent(x, y)
        
    def isInBounds(self, x: int, y: int) -> bool:
        if x < self.rowCount() and x >= 0 and y < self.columnCount() and y >= 0:
            return True
        return False

    def calculateAdjacent(self, x: int, y: int):
        if self.isInBounds(x + 1, y + 1):
            self._data[x + 1][y + 1][1] += 1
        if self.isInBounds(x + 1, y):
            self._data[x + 1][y][1] += 1
        if self.isInBounds(x + 1, y - 1):
            self._data[x + 1][y - 1][1] += 1
        if self.isInBounds(x, y + 1):
            self._data[x][y + 1][1] += 1
        if self.isInBounds(x, y - 1):
            self._data[x][y - 1][1] += 1
        if self.isInBounds(x - 1, y + 1):
            self._data[x - 1][y + 1][1] += 1
        if self.isInBounds(x - 1, y):
            self._data[x - 1][y][1] += 1
        if self.isInBounds(x - 1, y - 1):
            self._data[x - 1][y - 1][1] += 1      

    def rowCount(self):
        return len(self._data)

    def columnCount(self):
        return len(self._data[0])

if __name__ == "__main__":
    a = MinesweeperModel()
    a.populateData()