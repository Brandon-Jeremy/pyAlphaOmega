import numpy
from Piece import Piece
from enum import Enum

class MoveType(Enum):
    NORMAL = 1
    DOUBLE_PAWN_PUSH = 2
    CASTLE = 3
    EN_PASSANT = 4
    PROMOTION = 5
    CAPTURE = 6
    PROMOTION_CAPTURE = 7

class Move:
    def __init__(self, piece: Piece, color: str, start_tile: int, capture_tile: int, move_type: MoveType, promotion_piece: Piece=None, castle_side: str = None, captured_piece: Piece = None) -> None:
        self.piece = piece
        self.color = color
        self.start_tile = start_tile
        self.capture_tile = capture_tile
        self.type = move_type
        self.promoted_to = promotion_piece
        self.castle_side = castle_side
        self.captured_piece = captured_piece

    def __repr__(self) -> str:
        return f'{self.piece.get_symbol()} {self.start_tile} -> {self.capture_tile} [{self.type.name}]'