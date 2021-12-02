from PySide2.QtGui import QBrush, QColor
from PySide2.QtWidgets import QAbstractItemDelegate
from MinesweeperModel import *

class MinesweeperDelegate(QAbstractItemDelegate):
    def __init__(self, parent = None):
        super(MinesweeperDelegate, self).__init__(parent)
        

    def paint(self, painter, option, index):
        painter.drawRect(option.rect, )
        if index.data()[0] == FLAG:
            painter.drawText(option.rect, "F")
        elif index.data()[0] == DISPLAY:
            painter.drawText(option.rect, str(index.data()[1]))