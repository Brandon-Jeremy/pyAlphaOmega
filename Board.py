import numpy
from Piece import Piece

class Board:
    def __init__(self) -> None:
        self.board = numpy.zeros(64, dtype=object)
        self.setup_board()

    def setup_board(self) -> None:
        for i in range(8,16):
            self.board[i] = Piece('pawn', 'white')
        for i in range(48,56):
            self.board[i] = Piece('pawn', 'black')

        # Set up the rooks
        self.board[0] = self.board[7] = Piece('rook', 'white')
        self.board[56] = self.board[63] = Piece('rook', 'black')

        # Set up the knights
        self.board[1] = self.board[6] = Piece('knight', 'white')
        self.board[57] = self.board[62] = Piece('knight', 'black')

        # Set up the bishops
        self.board[2] = self.board[5] = Piece('bishop', 'white')
        self.board[58] = self.board[61] = Piece('bishop', 'black')

        # Set up the queens
        self.board[3] = Piece('queen', 'white')
        self.board[59] = Piece('queen', 'black')
        
        # Set up the kings
        self.board[4] = Piece('king', 'white')
        self.board[60] = Piece('king', 'black')

        # Display the initial board for debugging
        self.print_board()      

    def print_board(self) -> None:
        for i in range(7, -1, -1):
            print(self.board[i*8:(i+1)*8])

board = Board()
