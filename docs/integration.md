# Use PySideChessBoard in your project
Of course, you can use this widget

Example code: show the default board
```python
from PySide6.QtWidgets import QApplication
from PySideChessBoard.widgets.chessboard import 
import sys

app = QApplication(sys.argv)

board = ChessBoard()
board.show()

sys.exit(app.exec())
```
