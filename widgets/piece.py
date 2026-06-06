from PySide6.QtSvgWidgets import QGraphicsSvgItem

from PySide6.QtWidgets import QGraphicsSceneMouseEvent
from PySide6.QtGui import QPainter, QPen, QBrush, QColor, QRadialGradient
from PySide6.QtSvg import QSvgRenderer

from PySide6.QtCore import QPoint, QPointF, QTimer, Qt, QRectF, QPropertyAnimation, QEasingCurve, Property, Signal

class GPiece:
    pass

class GPiece(QGraphicsSvgItem):
    moveRequested = Signal(GPiece, int, int)
    showLegalMoves = Signal(str)
    hideLegalMoves = Signal()

    def __init__(self, piece_name: str, tile_size):
        super().__init__()

        self.tile_size = tile_size

        self.piece_type: str = piece_name
        
        self.color = self.piece_type[self.piece_type.index("_") + 1:]

        self._renderer = QSvgRenderer(f"widgets/pieces/{piece_name}.svg")
        self.setSharedRenderer(self._renderer)

        self.hovering = False
        self.dragging = False
        self.mouse_position = QPoint(0, 0)

        self.hover_paint_size = 0.0
        self.drag_bg_color = QColor(0, 0, 0, 0)
        self._paint_size_anim = None
        self._drag_bg_color_anim = None

        self.in_check = False

        self.right_click = False


        self.drag_start_pos = QPointF(0, 0)
        self.pending_move = QPointF(0, 0)

        self.annotation_color = 0

        self.setAcceptHoverEvents(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)

        self.setZValue(2)


    def setPieceType(self, new_type):
        self.piece_type = new_type
        self._renderer = QSvgRenderer(f"widgets/pieces/{new_type}.svg")
        self.setSharedRenderer(self._renderer)
        self.update()

    def getPieceType(self):
        return self.piece_type
    
    def getColor(self):
        return self.color


    def placeOnGrid(self):
        size = self.boundingRect().height()

        centered_x = self.pos().x() + (size // 2)
        centered_y = self.pos().y() + (size // 2)

        x = (centered_x // size) * size
        y = (centered_y // size) * size
        self.setPos(QPointF(x, y))


    def hoverEnterEvent(self, event):
        self.hovering = True
        self.animatePenSizeTo(8)
        return super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.hovering = False
        self.animatePenSizeTo(0)
        return super().hoverLeaveEvent(event)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):

        if event.button() == Qt.MouseButton.RightButton:
            self.right_click = True
            return

        self.right_click = False

        self.setZValue(3)

        self.drag_start_pos = self.pos()
        self.dragging = True

        self.animateDragBgColorTo(QColor(0, 0, 0, 50))

        self.mouse_position = event.screenPos()
        self.centerOnMouseMove(event)

        self.showLegalMoves.emit(self.data(Qt.ItemDataRole.UserRole))

        self.update()

        return super().mousePressEvent(event)
    
    def addAnnotation(self, modifiers):
        if self.right_click and self.hovering:
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

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent):
        if not self.dragging:
            if self.right_click:
                QTimer.singleShot(0, lambda m=event.modifiers(): self.addAnnotation(m))
            self.update()
            return
        
        self.hideLegalMoves.emit()

        self.setZValue(2)
        self.dragging = False
        self.placeOnGrid()
        self.pending_move = self.pos()

        self.animateDragBgColorTo(QColor(0, 0, 0, 0))

        self.setPos(self.drag_start_pos)
        self.moveRequested.emit(self, self.pending_move.x(), self.pending_move.y())

        self.update()
        return super().mouseReleaseEvent(event)

    def boundingRect(self):
        return QRectF(0, 0, self.tile_size, self.tile_size)


    def setInCheck(self, c):
        self.in_check = c
        self.update()

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):

        if not self.right_click:
            self.mouse_position = event.screenPos()
            self.centerOnMouseMove(event)

        return super().mouseMoveEvent(event)


    def centerOnMouseMove(self, event):
        if self.dragging:
            scene_position = event.scenePos()
            size = self.boundingRect().width()

            self.setPos(
                scene_position.x() - size / 2,
                scene_position.y() - size / 2
            )



    def animatePenSizeTo(self, s):
        self._paint_size_anim = QPropertyAnimation(self, b"hoverPenSizeProperty")

        self._paint_size_anim.setDuration(100)
        self._paint_size_anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        self._paint_size_anim.setStartValue(self.hover_paint_size)
        self._paint_size_anim.setEndValue(s)
        self._paint_size_anim.finished.connect(self._paint_size_anim.deleteLater)
        self._paint_size_anim.start()

    def animateDragBgColorTo(self, c):
        self._drag_bg_color_anim = QPropertyAnimation(self, b"dragBgColorProperty")

        self._drag_bg_color_anim.setDuration(150)
        self._drag_bg_color_anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        self._drag_bg_color_anim.setStartValue(self.drag_bg_color)
        self._drag_bg_color_anim.setEndValue(c)
        self._drag_bg_color_anim.finished.connect(self._drag_bg_color_anim.deleteLater)
        self._drag_bg_color_anim.start()

    def getHoverPaintSize(self):
        return self.hover_paint_size
    
    def setHoverPaintSize(self, s):
        self.hover_paint_size = s
        self.update()

    def getDragBgColor(self):
        return self.drag_bg_color
    
    def setDragBgColor(self, c):
        self.drag_bg_color = c
        self.update()

    hoverPenSizeProperty = Property(float, getHoverPaintSize, setHoverPaintSize)
    dragBgColorProperty = Property(QColor, getDragBgColor, setDragBgColor)



    def playPendingMove(self):
        self.setPos(self.pending_move)
        self.placeOnGrid()
        self.pending_move = QPointF(0, 0)

    def cancelPendingMove(self):
        self.pending_move = QPointF(0, 0)

    def paint(self, painter: QPainter, option, widget):
        paint_hover = True
        
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        if self.dragging or (self.drag_bg_color != QColor(0, 0, 0, 0)):
            
            painter.setBrush(QBrush(self.drag_bg_color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRect(self.boundingRect())

            if self.dragging:
                paint_hover = False

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

        if self.in_check:
            bouding_rect = self.boundingRect()

            center = QPointF(bouding_rect.width() / 2, bouding_rect.height() / 2)
            radial_gradient = QRadialGradient(center, bouding_rect.width())
            radial_gradient.setColorAt(0, QColor(255, 0, 0, 255))
            radial_gradient.setColorAt(1, QColor(255, 0, 0, 0))

            painter.setBrush(QBrush(radial_gradient))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRect(self.boundingRect())

        self._renderer.render(painter, self.boundingRect())


        if (self.hovering or self.hover_paint_size > 0.1) and paint_hover:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor("white"), self.hover_paint_size))
            painter.drawRect(self.boundingRect())

