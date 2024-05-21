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
        return piece_values.get(type, 0)