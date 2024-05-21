import numpy
from Piece import Piece
from Move import Move, MoveType

class Board:
    def __init__(self) -> None:
        self.board = numpy.full(64,None,dtype=object)
        # self.setup_board()
        self.active_color = 'white'
        self.castling_rights = 'KQkq'
        self.en_passant_square = '-'
        self.num_halfmoves = 0
        self.num_fullmoves = 1

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

    def setup_from_FEN(self, fen: str) -> None:

        def algebraic_to_index(algebraic: str) -> int:
            file = ord(algebraic[0]) - ord('a')
            rank = int(algebraic[1]) - 1
            return rank * 8 + file

        "r4rk1/pb1pnppp/n1p1pq2/1p4B1/1b1P1P2/2PQ3N/PP1NP1PP/2KR1B1R w - - 0 1"
        self.active_color = 'white' if fen.split(' ')[1] == 'w' else 'black'
        self.castling_rights = fen.split(' ')[2]
        self.en_passant_square = algebraic_to_index(fen.split(' ')[3])
        self.num_halfmoves = int(fen.split(' ')[4])
        self.num_fullmoves = int(fen.split(' ')[5])
        fen = fen.split(' ')[0]

        rank = 7
        file = 0
        for char in fen:
            if char == '/':
                rank -= 1
                file = 0
            elif char.isdigit():
                file += int(char)
            else:
                piece = Piece.get_piece_from_symbol(char)
                self.board[rank*8 + file] = piece
                file += 1
        pass

    def print_board(self) -> None:
        for i in range(7, -1, -1):
            row = self.board[i*8:(i+1)*8]
            print([str(piece) if piece is not None else 'o' for piece in row])


    def generate_pawn_moves(self, position, color):
        moves = []
        direction = 8 if color == 'white' else -8
        start_row = 1 if color == 'white' else 6

        # Single step forward
        forward_pos = position + direction
        print(forward_pos, "forward_pos")
        print(self.board[forward_pos], "self.board[forward_pos]")
        if 0 <= forward_pos < 64 and not self.board[forward_pos]:
            forward_move = Move(self.board[position], color, position, forward_pos, MoveType.NORMAL)
            moves.append(forward_move)
            
            # Double step forward from starting position
            if position // 8 == start_row:
                double_forward_pos = position + 2 * direction
                if not self.board[double_forward_pos]:
                    double_forward_move = Move(self.board[position], color, position, double_forward_pos, MoveType.DOUBLE_PAWN_PUSH)
                    moves.append(double_forward_move)

        # Captures
        for diag in [-1, 1]:
            capture_pos = position + direction + diag
            if 0 <= capture_pos < 64 and abs((capture_pos % 8) - (position % 8)) == 1:
                if self.board[capture_pos] and self.board[capture_pos].color != color:
                    capture_move = Move(self.board[position], color, position, capture_pos, MoveType.CAPTURE)
                    moves.append(capture_move)

        # En Passant 
        # TODO: Implement this

        return moves
    
    def generate_moves(self, position):
        piece = self.board[position]
        if not piece:
            print("No piece at position", position)
            return []
        
        if piece.type == 'pawn':
            print("Generating pawn moves")
            return self.generate_pawn_moves(position, piece.color)


board = Board()
board.setup_from_FEN("r4rk1/pb1pnppp/n3pq2/1ppP2B1/1b3P2/2PQ3N/PP1NP1PP/2KR1B1R w Kq c6 0 1")
board.print_board()
board.generate_moves(35)
