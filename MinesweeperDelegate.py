from PySide2.QtGui import QBrush, QColor, QPen, QTextOption
from PySide2.QtWidgets import QAbstractItemDelegate
from MinesweeperModel import *
from PySide2.QtCore import Qt

class MinesweeperDelegate(QAbstractItemDelegate):
    def __init__(self, parent = None):
        super(MinesweeperDelegate, self).__init__(parent)
        

    def paint(self, painter, option, index):
        painter.setPen(QPen("black"))
        if index.data()[0] == FLAG:
            painter.fillRect(option.rect, QColor("green"))
            painter.drawText(option.rect, Qt.AlignCenter, "F")
        elif index.data()[0] == DISPLAY:
            if index.data()[1] == MINE:
                painter.fillRect(option.rect, QColor("red"))
                painter.drawText(option.rect, Qt.AlignCenter, "M")
            else:
                colors = {0 : "black", 1 : "blue", 2 : "green", 3 : "red", 4 : "purple", 5 : "maroon", 6 : "turquoise", 7 : "black", 8 : "gray"}
                painter.setPen(QPen(colors[index.data()[1]]))
                painter.drawText(option.rect, Qt.AlignCenter, str(index.data()[1]))