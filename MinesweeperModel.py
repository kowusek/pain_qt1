from PySide2.QtCore import QAbstractTableModel

ROW_COUNT = 8
COLUMN_COUNT = 8

# item -> [display: int, value: int]

#display:
DISPLAY = 1
HIDE = 0
FLAG = -1

#value:
MINE = -1

class MinesweeperModel(QAbstractTableModel):
    def __init__(self):
        super.__init__(self)
        self._data = []

    def populateData(self):
        pass
        
    def rowCount(self):
        return len(self._data)

    def columnCount(self):
        return len(self._data[0])