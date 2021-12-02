from PySide2.QtWidgets import QApplication, QWidget, QLCDNumber
from PySide2.QtCore import QTimer
import sys

class TimeCounter:

    def __init__(self, display: QLCDNumber) -> None:
        self.count = 0
        self.display = display
        self.timer = QTimer(self.display)
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)
        self.showTime()

    def resetTime(self):
        self.count = 0
        self.display.display(self.count)

    def showTime(self):
        self.display.display(self.count)
        self.count += 1

if __name__ == "__main__":
    app = QApplication([])
    widget = QLCDNumber()
    timer = TimeCounter(widget)
    widget.show()
    sys.exit(app.exec_())