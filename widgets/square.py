from PySide6.QtWidgets import QGraphicsRectItem
from PySide6.QtGui import QPainter, Qt, QBrush, QColor, QMouseEvent
from PySide6.QtCore import QTimer

class GSquare(QGraphicsRectItem):
    def __init__(self, color):
        super().__init__()
        
        self.color = color
        self.setPen(Qt.PenStyle.NoPen)
        self.setBrush(QBrush(color))

        self.annotation_color = 0
        self.hovering = False
        self.is_right_click = False

        self.setAcceptHoverEvents(True)

        self.setZValue(0)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.RightButton:
            self.is_right_click = True
            return

        self.is_right_click = False

        return super().mousePressEvent(event)

    def addAnnotation(self, modifiers):
        if not self.hovering:
            return
        
        match modifiers:

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

    def hoverEnterEvent(self, event):
        self.hovering = True
        return super().hoverEnterEvent(event)
    
    def hoverLeaveEvent(self, event):
        self.hovering = False
        return super().hoverLeaveEvent(event)
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        if self.is_right_click:
            QTimer.singleShot(0, lambda m=event.modifiers(): self.addAnnotation(m))
        return super().mouseReleaseEvent(event)

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