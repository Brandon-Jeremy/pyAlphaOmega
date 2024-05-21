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

class Move:
    def __init__(self, piece: Piece, color: str, start_tile: int, capture_tile: int, move_type: MoveType) -> None:
        self.piece = piece
        self.color = color
        self.start_tile = start_tile
        self.capture_tile = capture_tile
        self.type = move_type

    def __repr__(self) -> str:
        return f'{self.piece.get_symbol()} {self.start_tile} -> {self.capture_tile} [{self.type.name}]'