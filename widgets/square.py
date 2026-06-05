from PySide6.QtWidgets import QGraphicsRectItem
from PySide6.QtGui import QPainter, Qt, QBrush, QColor, QMouseEvent

class GSquare(QGraphicsRectItem):
    def __init__(self, color):
        super().__init__()
        
        self.color = color
        self.setPen(Qt.PenStyle.NoPen)
        self.setBrush(QBrush(color))

        self.annotation_color = 0

        self.setZValue(0)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.RightButton:
            match event.modifiers():

                case Qt.KeyboardModifier.NoModifier:
                    if self.annotation_color != 0:
                        self.annotation_color = 0
                    else:
                        self.annotation_color = 1
                
                case Qt.KeyboardModifier.ShiftModifier:
                    self.annotation_color = 2
                
                case Qt.KeyboardModifier.ControlModifier:
                    self.annotation_color = 3
                
                case Qt.KeyboardModifier.AltModifier:
                    self.annotation_color = 4

            self.update()

        return super().mousePressEvent(event)

    def paint(self, painter: QPainter, option, widget):
        super().paint(painter, option, widget)

        if self.annotation_color != 0:
            color = QColor("#e35d5b")

            match self.annotation_color:
                case 1:
                    color = QColor("#e35d5b")
                case 2:
                    color = QColor("#68e35b")
                case 3:
                    color = QColor("#e6be49")
                case 4:
                    color = QColor("#49a4e6")

            color.setAlpha(200)

            painter.setBrush(QBrush(color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRect(self.boundingRect())