from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtGui import Qt, QColor, QPainter, QPen, QBrush, QPolygonF
from PySide6.QtCore import QRectF, QLineF, QPointF

class GArrow(QGraphicsItem):
    def __init__(self, start, end, color=QColor("#ffa600")):
        super().__init__()

        self.start = start
        self.end = end
        self.color = color
        self.setZValue(4)

    def boundingRect(self):
        return QRectF(self.start, self.end).normalized().adjusted(-30, -30, 30, 30)
    
    def paint(self, painter: QPainter, option, widget):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        pen = QPen(self.color, 12, Qt.PenStyle.SolidLine, Qt.PenCapStyle.FlatCap, Qt.PenJoinStyle.MiterJoin)
        painter.setPen(pen)
        painter.drawLine(self.start, self.end)

        line = QLineF(self.start, self.end)
        angle = line.angle()

        painter.save()
        painter.translate(self.end)
        painter.rotate(-angle)

        painter.setBrush(QBrush(self.color))

        triangle = QPolygonF([
            QPointF(0, 0),
            QPointF(-22, 12),
            QPointF(-22, -12)
        ])
        painter.drawPolygon(triangle)

        painter.restore()