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

    def algebraic_to_index(self, algebraic: str) -> int:
        file = ord(algebraic[0]) - ord('a')
        rank = int(algebraic[1]) - 1
        return rank * 8 + file
    
    def setup_from_FEN(self, fen: str) -> None:
        "r4rk1/pb1pnppp/n1p1pq2/1p4B1/1b1P1P2/2PQ3N/PP1NP1PP/2KR1B1R w - - 0 1"
        self.active_color = 'white' if fen.split(' ')[1] == 'w' else 'black'
        self.castling_rights = fen.split(' ')[2]
        self.en_passant_square = self.algebraic_to_index(fen.split(' ')[3])
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
            if forward_pos // 8 == 0 or forward_pos // 8 == 7:
                # Promotion
                promotion_move = Move(self.board[position], color, position, forward_pos, MoveType.PROMOTION)
                moves.append(promotion_move)
            else:
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
        enpassant_square = self.en_passant_square
        print(enpassant_square, "enpassant_square")
        if(enpassant_square == position + 9 and color=='white'):
            # En passant capture to the right of the pawn by WHITE
            enpassant_move = Move(self.board[position], color, position, enpassant_square, MoveType.EN_PASSANT)
            moves.append(enpassant_move)
        if(enpassant_square == position + 7 and color=='white'):
            # En passant capture to the left of the pawn by WHITE
            enpassant_move = Move(self.board[position], color, position, enpassant_square, MoveType.EN_PASSANT)
            moves.append(enpassant_move)
        if(enpassant_square == position - 9 and color=='black'):
            # En passant capture to the right of the pawn by BLACK
            enpassant_move = Move(self.board[position], color, position, enpassant_square, MoveType.EN_PASSANT)
            moves.append(enpassant_move)
        if(enpassant_square == position - 7 and color=='black'):
            # En passant capture to the left of the pawn by BLACK
            enpassant_move = Move(self.board[position], color, position, enpassant_square, MoveType.EN_PASSANT)
            moves.append(enpassant_move)

        return moves
    
    def generate_rook_moves(self, position, color):
        moves = []
        directions = [-8, 8, -1, 1]  # Vertical and horizontal directions

        for direction in directions:
            current_pos = position
            while True:
                current_pos += direction
                if current_pos < 0 or current_pos >= 64:
                    break
                if abs((current_pos % 8) - (position % 8)) > 1 and (direction == -1 or direction == 1):
                    break
                if self.board[current_pos]:
                    if self.board[current_pos].color != color:
                        move = Move(self.board[position], color, position, current_pos, MoveType.CAPTURE)
                        moves.append(move)
                    break
                move = Move(self.board[position], color, position, current_pos, MoveType.NORMAL)
                moves.append(move)
        return moves
    
    def generate_knight_moves(self, position, color):
        moves = []
        directions = [-17, -15, -10, -6, 6, 10, 15, 17]
        for direction in directions:
            current_pos = position + direction
            if current_pos < 0 or current_pos >= 64:
                continue
            if abs((current_pos % 8) - (position % 8)) > 2:
                continue
            if self.board[current_pos] and self.board[current_pos].color == color:
                continue
            if self.board[current_pos] and self.board[current_pos].color != color:
                move = Move(self.board[position], color, position, current_pos, MoveType.CAPTURE)
                moves.append(move)
            else:
                move = Move(self.board[position], color, position, current_pos, MoveType.NORMAL)
                moves.append(move)

        return moves
    
    def generate_bishop_moves(self, position, color):
        moves = []
        directions = [-9, -7, 7, 9]
        for direction in directions:
            current_pos = position
            while True:
                current_pos += direction
                if current_pos < 0 or current_pos >= 64:
                    break
                if abs((current_pos % 8) - (position % 8)) > 1:
                    break
                if self.board[current_pos]:
                    if self.board[current_pos].color != color:
                        move = Move(self.board[position], color, position, current_pos, MoveType.CAPTURE)
                        moves.append(move)
                    break
                move = Move(self.board[position], color, position, current_pos, MoveType.NORMAL)
                moves.append(move)

        return moves

    def generate_moves(self, position):
        piece = self.board[position]
        if not piece:
            print("No piece at position", position)
            return []
        
        if piece.type == 'pawn':
            print("Generating pawn moves")
            return self.generate_pawn_moves(position, piece.color)
        
        if piece.type == 'knight':
            print("Generating knight moves")
            return self.generate_knight_moves(position, piece.color)
        
        if piece.type == 'bishop':
            print("Generating bishop moves")
            return self.generate_bishop_moves(position, piece.color)
        
        if piece.type == 'rook':
            print("Generating rook moves")
            return self.generate_rook_moves(position, piece.color)

board = Board()
board.setup_from_FEN("r4rk1/pb1pnpp1/n3pq2/RppP2Bp/1b3P2/2PQ3N/PPN1P1PP/2K2B1R w Kq c6 0 1")
board.print_board()
moves = board.generate_moves(38)
print(moves)