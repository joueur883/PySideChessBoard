from PySide6.QtWidgets import QApplication

from widgets.chessboard import ChessBoard

app = QApplication()

board = ChessBoard()
board.setFen("8/P7/8/8/7k/8/8/4K3 w - - 0 1")
board.show()

app.exec()
