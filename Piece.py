import numpy

class Piece:
    def __init__(self, type:str, color:str) -> None:
        self.type = type
        self.color = color
        self.value = self.set_value()

    def __repr__(self) -> str:
        return self.get_symbol()
    
    def get_symbol(self) -> str:
        piece_symbols = {
            'pawn': 'P', 'rook': 'R', 'knight': 'N',
            'bishop': 'B', 'queen': 'Q', 'king': 'K'
        }
        symbol = piece_symbols.get(self.type, '?')
        return symbol if self.color == 'white' else symbol.lower()
    
    def set_value(self) -> int:
        piece_values = {
            'pawn': 1, 'rook': 5, 'knight': 3,
            'bishop': 3, 'queen': 9, 'king': 999
        }
        negate = -1 if self.color == 'black' else 1
        return piece_values.get(type, 0) * negate
    
    def get_piece_from_symbol(symbol:str) -> 'Piece':
        piece_types = {
            'P': 'pawn', 'R': 'rook', 'N': 'knight',
            'B': 'bishop', 'Q': 'queen', 'K': 'king'
        }
        color = 'black' if symbol.islower() else 'white'
        return Piece(piece_types[symbol.upper()], color)