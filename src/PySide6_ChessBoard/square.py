from PySide6.QtWidgets import QGraphicsRectItem
from PySide6.QtGui import QPainter, Qt, QBrush, QColor, QMouseEvent
from PySide6.QtCore import Property, QObject, QPropertyAnimation, QTimer, QEasingCurve, Signal

class GSquare(QObject, QGraphicsRectItem):
    pass

class GSquare(QObject, QGraphicsRectItem):
    def __init__(self, color):
        QObject.__init__(self)
        QGraphicsRectItem.__init__(self)
        
        self.color = color

        self.setPen(Qt.PenStyle.NoPen)
        self.setBrush(QBrush(color))

        self.annotation_color = 0
        self.hovering = False
        self.is_right_click = False

        self.is_legal_move = False
        self._legal_move_color = QColor(0, 0, 0, 0)
        self.legal_move_color_anim = None

        self._annotation_color_alpha = 0
        self.annotation_color_alpha_anim = None

        self.setCursor(Qt.CursorShape.ArrowCursor)

        self.setAcceptHoverEvents(True)

        self.setZValue(0)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.RightButton:
            self.is_right_click = True
            return

        self.is_right_click = False

        return super().mousePressEvent(event)

    def setIsLegalMove(self, is_legal):
        self.is_legal_move = is_legal

        if is_legal:
            self.setCursor(Qt.CursorShape.PointingHandCursor)
            self.tweenLegalMoveColorTo(QColor(0, 0, 0, 50))
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)
            self.tweenLegalMoveColorTo(QColor(0, 0, 0, 0))

        self.update()

    def addAnnotation(self, modifiers):
        if not self.hovering:
            return

        added = True

        match modifiers:

            case Qt.KeyboardModifier.NoModifier:
                if self.annotation_color != 0 and self.annotation_color == 1:
                    self.annotation_color = 0
                    added = False
                else:
                    self.annotation_color = 1
                
            case Qt.KeyboardModifier.ShiftModifier:
                self.annotation_color = 2
                
            case Qt.KeyboardModifier.ControlModifier:
                self.annotation_color = 3
                
            case Qt.KeyboardModifier.AltModifier:
                self.annotation_color = 4

        if added:
            self.tweenAnnotationColorAlphaTo(200)
        else:
            self.tweenAnnotationColorAlphaTo(0)

        self.update()

    def clearColorAnnotation(self):
        self.annotation_color = 0
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

    
    def getLegalMoveColor(self):
        return self._legal_move_color
    
    def setLegalMoveColor(self, c):
        self._legal_move_color = c
        self.update()

    def getAnnotationColorAlpha(self):
        return self._annotation_color_alpha
    
    def setAnnotationColorAlpha(self, a):
        self._annotation_color_alpha = a
        self.update()

    def tweenLegalMoveColorTo(self, color):
        self.legal_move_color_anim = QPropertyAnimation(self, b"legalMoveColorP")
        self.legal_move_color_anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.legal_move_color_anim.setDuration(150)

        self.legal_move_color_anim.setStartValue(self._legal_move_color)
        self.legal_move_color_anim.setEndValue(color)

        self.legal_move_color_anim.start()

    def tweenAnnotationColorAlphaTo(self, alpha):
        self.annotation_color_alpha_anim = QPropertyAnimation(self, b"annotationColorAlphaP")
        self.annotation_color_alpha_anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.annotation_color_alpha_anim.setDuration(150)

        self.annotation_color_alpha_anim.setStartValue(self._annotation_color_alpha)
        self.annotation_color_alpha_anim.setEndValue(alpha)

        self.annotation_color_alpha_anim.start()



    legalMoveColorP = Property(QColor, getLegalMoveColor, setLegalMoveColor)
    annotationColorAlphaP = Property(int, getAnnotationColorAlpha, setAnnotationColorAlpha)



    def paint(self, painter: QPainter, option, widget):
        super().paint(painter, option, widget)

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self.annotation_color != 0 or self._annotation_color_alpha > 5:
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

            color.setAlpha(self._annotation_color_alpha)

            painter.setBrush(QBrush(color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRect(self.boundingRect())

        if self.is_legal_move or self._legal_move_color != QColor(0, 0, 0, 0):
            painter.setBrush(QBrush(self._legal_move_color))
            painter.setPen(Qt.PenStyle.NoPen)

            painter.drawEllipse(self.boundingRect())
