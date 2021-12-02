# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
from PySide2.QtWidgets import QApplication, QDialog, QHeaderView, QMainWindow, QMessageBox
from PySide2.QtCore import QFile, QEvent, Qt
from UiLoader import loadUi
from MinesweeperModel import MinesweeperModel, gameOver, gameWon#, updateFlagCount
from MinesweeperDelegate import MinesweeperDelegate
from Counters import TimeCounter

class Minesweeper(QMainWindow):
    def __init__(self, model: MinesweeperModel, delegate: MinesweeperDelegate):
        super(Minesweeper, self).__init__()
        self.load_ui("Minesweeper.ui", self)
        self.clock = TimeCounter(self.Stopwatch)
        self.model = model

        self.Minefiled.setModel(model)
        self.Minefiled.setItemDelegate(delegate)

        self.Minefiled.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.Minefiled.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # updateFlagCount.signal.connect(self.FlagCount.display)
        gameOver.signal.connect(self.clock.stopTime)
        gameOver.signal.connect(self.gameOver)
        gameWon.signal.connect(self.clock.stopTime)
        gameWon.signal.connect(self.gameWon)
        self.action_New_Game.triggered.connect(model.newGame)
        self.action_New_Game.triggered.connect(self.clock.resetTime)
        self.NewGameButton.clicked.connect(model.newGame)
        self.NewGameButton.clicked.connect(self.clock.resetTime)
        self.Minefiled.children()[0].installEventFilter(self)

        self.FlagCount.display("10")

    def gameOver(self):
        gameOverWindow = QMessageBox(self)
        gameOverWindow.setWindowTitle("Game Lost!")
        gameOverWindow.setText("You have lost the game!")
        button = gameOverWindow.exec_()
        if button == QMessageBox.Ok:
           self.model.newGame()
           self.clock.resetTime()

    def gameWon(self):
        gameWonWindow = QMessageBox(self)
        gameWonWindow.setWindowTitle("Game Won!")
        gameWonWindow.setText("Congratulations, you have won the game!")
        button = gameWonWindow.exec_()
        if button == QMessageBox.Ok:
           self.model.newGame()
           self.clock.resetTime()
    
    def load_ui(self, filename, widget):
        path = os.fspath(Path(__file__).resolve().parent / filename)
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loadUi(ui_file, widget)
        ui_file.close()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            row = self.Minefiled.rowAt(event.y())
            column = self.Minefiled.columnAt(event.x())
            if event.button() == Qt.RightButton:
                model.setAsFlaged(row, column)
            elif event.button() == Qt.LeftButton:
                model.setAsClicked(row, column)
        
        return super(Minesweeper, self).eventFilter(obj, event)

if __name__ == "__main__":
    app = QApplication([])
    model = MinesweeperModel()
    delegate = MinesweeperDelegate(model)
    widget = Minesweeper(model, delegate)
    widget.show()
    sys.exit(app.exec_())