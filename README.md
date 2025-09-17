# Minesweeper Game (Python / PySide2)

A desktop Minesweeper implementation using **Python** and **PySide2**. The game includes a live timer, flag counter, and interactive minefield with dynamic win/loss handling.

---

## Features

* **Classic Minesweeper gameplay**
  Click cells to reveal them, right-click to place flags, and avoid mines to win.

* **Timer**
  Tracks the duration of each game using a `QLCDNumber` display.

* **Flag Counter**
  Displays the number of remaining flags.

* **Dynamic UI**
  Built using `.ui` files loaded at runtime with `UiLoader`.

* **New Game Support**
  Reset the board and timer with a button or menu action.

* **Win/Loss Notifications**
  Pop-up dialogs notify the player when the game is won or lost.

---

## File Overview

* **`Counters.py`**
  Implements the `TimeCounter` class to manage the stopwatch.

  * `showTime()`: Updates the displayed time.
  * `resetTime()`: Resets the timer to zero.
  * `stopTime()`: Stops the timer.

* **`Minesweeper.py`**
  Main game window implementation.

  * Integrates `MinesweeperModel` for game logic.
  * Uses `MinesweeperDelegate` for custom cell rendering.
  * Handles user input (left/right clicks) and events.
  * Connects signals for game events and UI updates.

* **`MinesweeperModel.py`**
  Implements the game logic using `QAbstractTableModel`.

  * Maintains the minefield data, including cell display state and values.
  * Handles cell clicks, flag placement, and win/loss detection.
  * Signals: `gameOver`, `gameWon`, `updateFlagCount`.

* **`MinesweeperDelegate.py`**
  Custom delegate for rendering minefield cells.

  * Displays flags in green, mines in red, and numbers with color coding.

* **`UiLoader.py`**
  Dynamically loads `.ui` files into Python objects.

  * Supports existing base instances for integration with PySide2.
  * Handles custom widgets promoted in Qt Designer.

* **`Minesweeper.ui`**
  Qt Designer file defining the main window layout:

  * `QLCDNumber` for flag count and stopwatch.
  * `QTableView` for the minefield.
  * `QPushButton` for starting a new game.
  * Menu bar with "Game" menu for New Game and Exit actions.

---

## Installation

1. Install Python 3.8+
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Ensure all files (`.py` and `.ui`) are in the same directory.

---

## Running the Game

```bash
python Minesweeper.py
```

* Click **left mouse button** to reveal a cell.
* Click **right mouse button** to place or remove a flag.
* Press **New Game** to reset the game and timer.

---

## Notes

* The minefield is an 8x8 grid with 10 mines by default.
* The game uses a model-view-delegate architecture for flexibility and separation of UI and logic.
* The timer automatically stops on game over or win.
