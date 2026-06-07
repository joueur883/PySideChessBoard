from PySide6.QtWidgets import *
from PySide6.QtGui import QColor, QAction, QIcon, QKeyEvent
from PySide6.QtCore import QPoint, QPointF, QRect, QRectF, QSize, QTimer, Qt

from PySide6_ChessBoard.arrow import GArrow
from PySide6_ChessBoard.piece import GPiece
from PySide6_ChessBoard.square import GSquare

import pathlib
import os

import chess
import chess.engine

class ChessBoard(QGraphicsView):
    def __init__(self):
        super().__init__()


        self.gscene = QGraphicsScene(self)
        self.setScene(self.gscene)

        self.pieces_icon_path = pathlib.Path(os.path.abspath(__file__))
        self.pieces_icon_path = str(self.pieces_icon_path.parent / "pieces")

        self.tile_size = 80


        self.is_white_view = True

        self.show_legal_moves = True


        self.white_square_color = QColor("#F0D9B5")
        self.black_square_color = QColor("#B88C67")

        self.mouse_position = QPoint(0, 0)

        self.square_instances_dict: dict[str, GSquare] = {}
        self.pieces_instances_dict: dict[str, GPiece] = {}
        self.king_in_check_instance = None

        self.pieces_color_map = {
            chess.WHITE: "white",
            chess.BLACK: "black"
        }

        self.columns_letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
        self.rows_numbers = [1, 2, 3, 4, 5, 6, 7, 8]

        self.moves_history = []
        self.timeline_pos = 0

        self.arrow_start_pos = QPointF(0, 0)
        self.arrow_end_pos = QPointF(0, 0)

        self.arrows_pos = []
        self.arrows_instances_dict: dict[str, GArrow] = {}

        self.board = chess.Board()

        self.resetBoard()



    def setFen(self, fen: str) -> None:
        self.board.set_fen(fen)
        self.buildAndRenderBoard()

    def resetBoard(self) -> None:
        self.board.reset()
        self.moves_history.clear()
        self.moves_history.append(self.board.fen())

        self.buildAndRenderBoard()

    def setIsWhiteView(self, b: bool) -> None:
        self.is_white_view = b
        self.buildAndRenderBoard()

    def setTileSize(self, s: int) -> None:
        self.tile_size = s
        self.buildAndRenderBoard()

    def setShowLegalMoves(self, s: bool) -> None:
        self.show_legal_moves = s

    def setMovesHistory(self, h: list[str]) -> None:
        self.moves_history = h

    def setTimelinePosition(self, p: int) -> None:
        self.timeline_pos = p
        self.reRenderLater(self.moves_history[self.timeline_pos])


    def squareNameFromView(self, row, column):
        if self.is_white_view:
            file = column
            rank = 7 - row
        else:
            file =  7 - column
            rank = row
        
        return (
            self.columns_letters[file] +
            str(rank + 1)
        )


    def mouseMoveEvent(self, event):
        self.mouse_position = event.pos()
        return super().mouseMoveEvent(event)
    
    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        if event.button() == Qt.MouseButton.RightButton:
            mapped = self.mapToScene(event.pos())
            self.arrow_start_pos = self.posToSquareCoord(int(mapped.x()), int(mapped.y()))

        return super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent):
        if event.button() == Qt.MouseButton.RightButton:

            mapped = self.mapToScene(event.pos())
            
            self.arrow_end_pos = self.posToSquareCoord(round(mapped.x()), round(mapped.y()))

            if self.arrow_start_pos.strip() == "" or self.arrow_end_pos.strip() == "":
                return
            
            if self.arrow_start_pos != self.arrow_end_pos:
                if not f"{self.arrow_start_pos}{self.arrow_end_pos}" in self.arrows_pos:
                    self.arrows_pos.append(f"{self.arrow_start_pos}{self.arrow_end_pos}")

                    start_square_pos = self.square_instances_dict[self.arrow_start_pos].pos()
                    end_square_pos = self.square_instances_dict[self.arrow_end_pos].pos()

                    centered_sx = start_square_pos.x() + self.tile_size / 2
                    centered_sy = start_square_pos.y() + self.tile_size / 2
                    centered_ex = end_square_pos.x() + self.tile_size / 2
                    centered_ey = end_square_pos.y() + self.tile_size / 2

                    arrow = GArrow(QPointF(centered_sx, centered_sy), QPointF(centered_ex, centered_ey))
                    self.arrows_instances_dict[f"{self.arrow_start_pos}{self.arrow_end_pos}"] = arrow

                    self.gscene.addItem(arrow)
                else:
                    if f"{self.arrow_start_pos}{self.arrow_end_pos}" in self.arrows_instances_dict:
                        instance = self.arrows_instances_dict[f"{self.arrow_start_pos}{self.arrow_end_pos}"]

                        self.gscene.removeItem(instance)

                        del self.arrows_instances_dict[f"{self.arrow_start_pos}{self.arrow_end_pos}"]
                        self.arrows_pos.remove(f"{self.arrow_start_pos}{self.arrow_end_pos}")


        return super().mouseReleaseEvent(event)
    
    def keyPressEvent(self, event: QKeyEvent):
        
        key = event.key()

        if key == Qt.Key.Key_Right:
            if self.timeline_pos + 1 <= len(self.moves_history) - 1:
                self.timeline_pos += 1
                self.reRenderLater(custom_fen=self.moves_history[self.timeline_pos])
        elif key == Qt.Key.Key_Left:
            if self.timeline_pos >= 1:
                self.timeline_pos -= 1
                self.reRenderLater(custom_fen=self.moves_history[self.timeline_pos])
        elif key == Qt.Key.Key_Up:
            if self.timeline_pos < len(self.moves_history) - 1:
                self.timeline_pos = len(self.moves_history) - 1
                self.reRenderLater(custom_fen=self.moves_history[self.timeline_pos])
        elif key == Qt.Key.Key_Down:
            if self.timeline_pos != 0:
                self.timeline_pos = 0
                self.reRenderLater(custom_fen=self.moves_history[self.timeline_pos])

        return super().keyPressEvent(event)


    def posToSquareCoord(self, x, y):
        column = x // self.tile_size
        row = y // self.tile_size



        try:
            if self.is_white_view:
                return self.columns_letters[column] + str(self.rows_numbers[7 - row])
            return self.columns_letters[7 - column] + str(self.rows_numbers[row])
        except Exception as e:
            print(e)
            return ""

    def getLegalMovesStrFromSquare(self, square) -> list[str]:
        result = []
        
        for legal_move in self.board.legal_moves:
            if legal_move.from_square == square:
                result.append(str(legal_move)[2:])
        
        return result


    def playMoveFromStr(self, move_str):
        if len(move_str) == 4:
            part_1 = move_str[0:2]
            part_2 = move_str[2:4]

            if part_1 in self.pieces_instances_dict:
                self.playMoveWithPiece(self.pieces_instances_dict[part_1], False, part_2, True)

    def playMoveWithPiece(self, piece_instance: GPiece, is_pending_move, new_square_name=None, push=True):
        
        piece_square = chess.parse_square(piece_instance.data(Qt.ItemDataRole.UserRole))

        piece_square_name = chess.square_name(piece_square)
        
        turn = self.board.turn

        move = chess.Move.from_uci(piece_square_name + new_square_name)

        if self.king_in_check_instance is not None:
            self.king_in_check_instance.setInCheck(False)
            self.king_in_check_instance = None


        if "pawn" in piece_instance.getPieceType() and new_square_name[1] in ("1", "8"): # Promotion

            piece_color = piece_instance.getColor()
            if piece_color == "white" and new_square_name[1] == "1":
                piece_instance.cancelPendingMove()
                return
            elif piece_color == "black" and new_square_name[1] == "8":
                piece_instance.cancelPendingMove()
                return
            
            menu = QMenu()

            queen_action = QAction("Queen")
            queen_action.setIcon(QIcon(f"{self.pieces_icon_path}/queen_{piece_color}.svg"))

            rook_action = QAction("Rook")
            rook_action.setIcon(QIcon(f"{self.pieces_icon_path}/rook_{piece_color}.svg"))

            bishop_action = QAction("Bishop")
            bishop_action.setIcon(QIcon(f"{self.pieces_icon_path}/bishop_{piece_color}.svg"))

            knight_action = QAction("Knight")
            knight_action.setIcon(QIcon(f"{self.pieces_icon_path}/knight_{piece_color}.svg"))

            menu.addAction(queen_action)
            menu.addAction(rook_action)
            menu.addAction(bishop_action)
            menu.addAction(knight_action)

            selected_action = menu.exec(self.mapToGlobal(self.mouse_position))

            if selected_action is None:
                piece_instance.cancelPendingMove()
                return
            
            piece_color = piece_instance.getColor()

            if selected_action == queen_action:
                move.promotion = chess.QUEEN
                piece_instance.setPieceType(f"queen_{piece_color}")
            elif selected_action == rook_action:
                move.promotion = chess.ROOK
                piece_instance.setPieceType(f"rook_{piece_color}")
            elif selected_action == bishop_action:
                move.promotion = chess.BISHOP
                piece_instance.setPieceType(f"bishop_{piece_color}")
            else:
                move.promotion = chess.KNIGHT
                piece_instance.setPieceType(f"knight_{piece_color}")

        if self.board.is_capture(move):

            if self.board.is_en_passant(move):
                captured_square = chess.square(
                    chess.square_file(move.to_square) - 8,
                    chess.square_rank(move.to_square)
                )

                captured_name = chess.square_name(captured_square)

                if captured_name in self.pieces_instances_dict:
                    piece_to_remove = self.pieces_instances_dict[captured_name]
                    self.gscene.removeItem(piece_to_remove)
                    del self.pieces_instances_dict[captured_name]

            else:

                if new_square_name in self.pieces_instances_dict:
                    piece_to_remove = self.pieces_instances_dict[new_square_name]
                    self.gscene.removeItem(piece_to_remove)
                    del self.pieces_instances_dict[new_square_name]

        elif self.board.is_castling(move):
            
            if self.board.is_kingside_castling(move):
                if turn == chess.WHITE:
                    if "h1" in self.pieces_instances_dict:
                        self.playMoveWithPiece(self.pieces_instances_dict["h1"], False, "f1", False)
                        self.board.turn = chess.WHITE
                else:
                    if "h8" in self.pieces_instances_dict:
                        self.playMoveWithPiece(self.pieces_instances_dict["h8"], False, "f8", False)
                        self.board.turn = chess.BLACK
            else:
                if turn == chess.WHITE:
                    if "a1" in self.pieces_instances_dict:
                        self.playMoveWithPiece(self.pieces_instances_dict["a1"], False, "d1", False)
                        self.board.turn = chess.WHITE
                else:
                    if "a8" in self.pieces_instances_dict:
                        self.playMoveWithPiece(self.pieces_instances_dict["a8"], False, "d8", False)
                        self.board.turn = chess.BLACK
        

        if push:
            self.board.push(move)
            self.moves_history.append(self.board.fen())

            if self.timeline_pos + 1 < len(self.moves_history) - 1:
                self.timeline_pos = len(self.moves_history) - 1
                self.reRenderLater()
            else:
                self.timeline_pos += 1

        piece_instance.setData(Qt.ItemDataRole.UserRole, new_square_name)
        self.pieces_instances_dict[new_square_name] = piece_instance
        self.pieces_instances_dict.pop(piece_square_name)

        if is_pending_move:
            piece_instance.playPendingMove()
        else:
            square_instance = self.square_instances_dict[new_square_name]
            new_piece_pos = square_instance.pos()
            piece_instance.setPos(new_piece_pos)

        if self.board.is_check():
            king_square = chess.square_name(self.board.king(self.board.turn))
            if king_square in self.pieces_instances_dict:
                king_piece_instance = self.pieces_instances_dict[king_square]
                king_piece_instance.setInCheck(True)
                self.king_in_check_instance = king_piece_instance


    def playOrCancelMove(self, piece_instance: GPiece, new_x, new_y):
        new_coords = self.posToSquareCoord(new_x, new_y)
        
        new_square = chess.parse_square(new_coords)

        piece_data = piece_instance.data(Qt.ItemDataRole.UserRole)

        piece_square = chess.parse_square(piece_data)
        legal_moves_list = self.getLegalMovesStrFromSquare(piece_square)

        if len(legal_moves_list) == 0:
            piece_instance.cancelPendingMove()
            return
        
        new_square_name = chess.square_name(new_square)
        piece_square_name = chess.square_name(piece_square)

        
        is_promotion = "pawn" in piece_instance.getPieceType() and new_coords[1] in ("1", "8")

        if not new_square_name in legal_moves_list and not is_promotion:
            return
        
        self.playMoveWithPiece(piece_instance, True, new_square_name)
        

    def showLegalMovesFromSquare(self, square_coord):
        if not self.show_legal_moves:
            return

        square = chess.parse_square(square_coord)
        legal_moves = self.getLegalMovesStrFromSquare(square)

        if len(legal_moves) == 0:
            return
        
        for legal_move in legal_moves:
            if legal_move in self.square_instances_dict:
                square_instance = self.square_instances_dict[legal_move]
                square_instance.setIsLegalMove(True)

    def hideLegalMoves(self):
        if not self.show_legal_moves:
            return

        for square_coord, square in self.square_instances_dict.items():
            square.setIsLegalMove(False)
        





    def reRenderLater(self, custom_fen=""):
        QTimer.singleShot(0, lambda: self.buildAndRenderBoard(custom_fen=custom_fen))
        

    def buildAndRenderBoard(self, custom_fen=""):
        self.gscene.clear()
        
        self.arrows_pos = []
        self.arrows_instances_dict = {}

        self.square_instances_dict = {}
        self.pieces_instances_dict = {}

        self.square_colors = [self.white_square_color, self.black_square_color]
        color_i = 0

        x_pos = 0
        y_pos = 0

        _board = self.board

        if custom_fen != "":
            _board = chess.Board()
            _board.set_fen(custom_fen)

        for row in range(8):
            for column in range(8):

                tile_coord_str = self.squareNameFromView(row, column)
                # Square
                square = GSquare(self.square_colors[color_i % 2])
                square.setRect(QRectF(0, 0, self.tile_size, self.tile_size))
                square.setPos(QPoint(x_pos, y_pos))
                self.gscene.addItem(square)

                square.setData(Qt.ItemDataRole.UserRole, tile_coord_str)
                self.square_instances_dict[tile_coord_str] = square


                # Piece
                piece_at_square = None

                if self.is_white_view:
                    piece_at_square = _board.piece_at(chess.square(column, 7 - row))
                else:
                    piece_at_square = _board.piece_at(chess.square(7 - column, row))
                
                if piece_at_square is not None:
                    color_str = self.pieces_color_map[piece_at_square.color]

                    piece_x = column * self.tile_size
                    piece_y = row * self.tile_size

                    piece = GPiece(f"{chess.piece_name(piece_at_square.piece_type)}_{color_str}", self.tile_size)
                    piece.setPos(QPointF(piece_x, piece_y))
                    self.gscene.addItem(piece)

                    piece.moveRequested.connect(self.playOrCancelMove)
                    piece.showLegalMoves.connect(self.showLegalMovesFromSquare)
                    piece.hideLegalMoves.connect(self.hideLegalMoves)

                    piece.setData(Qt.ItemDataRole.UserRole, tile_coord_str)
                    self.pieces_instances_dict[tile_coord_str] = piece

                x_pos += self.tile_size
                color_i += 1

            x_pos = 0
            y_pos += self.tile_size
            color_i += 1
