# Use PySide6-ChessBoard in your project

## Example code: show the default board
```python
from PySide6.QtWidgets import QApplication
from PySide6_ChessBoard.chessboard import ChessBoard
import sys

app = QApplication(sys.argv)

board = ChessBoard()
board.show()

sys.exit(app.exec())
```
