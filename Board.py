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

        self.move_history = []

    def switch_turn(self):
        self.active_color = 'black' if self.active_color == 'white' else 'white'

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
        "rnb1kbnr/pp2qppp/2p5/4p3/2BP1p2/2N2N2/PPP3PP/R1BQK2R w KQkq - 2 9"
        self.active_color = 'white' if fen.split(' ')[1] == 'w' else 'black'
        self.castling_rights = fen.split(' ')[2]
        self.en_passant_square = self.algebraic_to_index(fen.split(' ')[3]) if fen.split(' ')[3] != '-' else '-'
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
                for i in range(4):
                    promotion_piece = ['queen', 'rook', 'bishop', 'knight'][i]
                    promotion_move = Move(self.board[position], color, position, forward_pos, MoveType.PROMOTION, Piece(promotion_piece, color))
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
                    if capture_pos // 8 == 0 or capture_pos // 8 == 7:
                    # Promotion and capture
                        for i in range(4):
                            promotion_piece = ['queen', 'rook', 'bishop', 'knight'][i]
                            promotion_capture_move = Move(self.board[position], color, position, capture_pos, MoveType.PROMOTION_CAPTURE, promotion_piece=Piece(promotion_piece, color),captured_piece=self.board[capture_pos])
                            moves.append(promotion_capture_move)
                    else:
                        capture_move = Move(self.board[position], color, position, capture_pos, MoveType.CAPTURE, captured_piece=self.board[capture_pos])
                        moves.append(capture_move)

        # En Passant
        enpassant_square = self.en_passant_square
        print(enpassant_square, "enpassant_square")
        if(enpassant_square == position + 9 and color=='white'):
            # En passant capture to the right of the pawn by WHITE
            enpassant_move = Move(self.board[position], color, position, enpassant_square, MoveType.EN_PASSANT, captured_piece=Piece('pawn', 'black'))
            moves.append(enpassant_move)
        if(enpassant_square == position + 7 and color=='white'):
            # En passant capture to the left of the pawn by WHITE
            enpassant_move = Move(self.board[position], color, position, enpassant_square, MoveType.EN_PASSANT, captured_piece=Piece('pawn', 'black'))
            moves.append(enpassant_move)
        if(enpassant_square == position - 9 and color=='black'):
            # En passant capture to the right of the pawn by BLACK
            enpassant_move = Move(self.board[position], color, position, enpassant_square, MoveType.EN_PASSANT, captured_piece=Piece('pawn', 'white'))
            moves.append(enpassant_move)
        if(enpassant_square == position - 7 and color=='black'):
            # En passant capture to the left of the pawn by BLACK
            enpassant_move = Move(self.board[position], color, position, enpassant_square, MoveType.EN_PASSANT, captured_piece=Piece('pawn', 'white'))
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
                        move = Move(self.board[position], color, position, current_pos, MoveType.CAPTURE, captured_piece=self.board[current_pos])
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
                move = Move(self.board[position], color, position, current_pos, MoveType.CAPTURE, captured_piece=self.board[current_pos])
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
                        move = Move(self.board[position], color, position, current_pos, MoveType.CAPTURE, captured_piece=self.board[current_pos])
                        moves.append(move)
                    break
                move = Move(self.board[position], color, position, current_pos, MoveType.NORMAL)
                moves.append(move)

        return moves
    
    def generate_queen_moves(self, position, color):
        moves = []
        directions = [-9, -8, -7, -1, 1, 7, 8, 9]
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
                        move = Move(self.board[position], color, position, current_pos, MoveType.CAPTURE, captured_piece=self.board[current_pos])
                        moves.append(move)
                    break
                move = Move(self.board[position], color, position, current_pos, MoveType.NORMAL)
                moves.append(move)

        return moves
    
    def generate_king_moves(self, position, color):
        moves = []
        directions = [-9, -8, -7, -1, 1, 7, 8, 9]
        for direction in directions:
            current_pos = position + direction
            if current_pos < 0 or current_pos >= 64:
                continue
            if abs((current_pos % 8) - (position % 8)) > 1:
                continue
            if self.board[current_pos] and self.board[current_pos].color == color:
                continue
            if self.board[current_pos] and self.board[current_pos].color != color:
                move = Move(self.board[position], color, position, current_pos, MoveType.CAPTURE, captured_piece=self.board[current_pos])
                moves.append(move)
            else:
                move = Move(self.board[position], color, position, current_pos, MoveType.NORMAL)
                moves.append(move)

        # Castling
        if color == 'white':
            if 'K' in self.castling_rights and not self.board[5] and not self.board[6]:
                move = Move(self.board[position], color, position, position + 2, MoveType.CASTLE, castle_side='K')
                moves.append(move)
            if 'Q' in self.castling_rights and not self.board[1] and not self.board[2] and not self.board[3]:
                move = Move(self.board[position], color, position, position - 2, MoveType.CASTLE, castle_side='Q')
                moves.append(move)

        if color == 'black':
            if 'k' in self.castling_rights and not self.board[61] and not self.board[62]:
                move = Move(self.board[position], color, position, position + 2, MoveType.CASTLE, castle_side='k')
                moves.append(move)
            if 'q' in self.castling_rights and not self.board[57] and not self.board[58] and not self.board[59]:
                move = Move(self.board[position], color, position, position - 2, MoveType.CASTLE, castle_side='q')
                moves.append(move)

        return moves
    
    def make_move(self, move: Move) -> bool:
        if move.piece.type == 'king':
            if move.type == MoveType.CASTLE:
                print("Castling move")
                if move.color == 'white':
                    if move.castle_side == 'K':
                        self.board[5] = self.board[7]
                        self.board[7] = None
                    else:
                        self.board[3] = self.board[0]
                        self.board[0] = None
                else:
                    if move.castle_side == 'k':
                        self.board[61] = self.board[63]
                        self.board[63] = None
                    else:
                        self.board[59] = self.board[56]
                        self.board[56] = None

        self.board[move.capture_tile] = self.board[move.start_tile]
        self.board[move.start_tile] = None

        if move.piece.type == 'pawn':
            self.num_halfmoves = 0
            if move.type == MoveType.EN_PASSANT:
                if move.color == 'white':
                    self.board[move.capture_tile - 8] = None
                else:
                    self.board[move.capture_tile + 8] = None
            if move.type == MoveType.DOUBLE_PAWN_PUSH:
                self.en_passant_square = move.capture_tile
            elif move.type == MoveType.PROMOTION:
                self.board[move.capture_tile] = move.promoted_to
                self.num_halfmoves = 0

        # At the end of the move switch colors. Append to history, and add to halftime + fulltime coutners [if color is black]
        if move.color == 'black':
            self.num_fullmoves+=1

        self.num_halfmoves+=0.5 if move.piece.type != 'pawn' else 0
        self.move_history.append(move)
        self.switch_turn()

        return True
    
    def undo_move(self) -> bool: 
        if not self.move_history:
            return False

        move = self.move_history.pop()
        self.board[move.start_tile] = move.piece
        self.board[move.capture_tile] = move.captured_piece

        if move.type == MoveType.EN_PASSANT:
            if move.color == 'white':
                self.board[move.capture_tile - 8] = Piece('pawn', 'black')
            else:
                self.board[move.capture_tile + 8] = Piece('pawn', 'white')

        if move.type == MoveType.PROMOTION:
            self.board[move.start_tile] = Piece('pawn', move.color)

        # Castling also needs to be undone where king moves back to original spot
        if move.type == MoveType.CASTLE:
            if move.castle_side == 'K':
                self.board[4] = Piece('king', move.color)
                self.board[7] = Piece('rook', move.color)

                self.board[5] = self.board[6] = None
            elif move.castle_side == 'Q':
                self.board[4] = Piece('king', move.color)
                self.board[0] = Piece('rook', move.color)

                self.board[1] = self.board[2] = self.board[3] = None
            elif move.castle_side == 'k':
                self.board[60] = Piece('king', move.color)
                self.board[63] = Piece('rook', move.color)

                self.board[61] = self.board[62] = None
            elif move.castle_side == 'q':
                self.board[60] = Piece('king', move.color)
                self.board[56] = Piece('rook', move.color)

                self.board[57] = self.board[58] = self.board[59] = None

        self.switch_turn()

        return True

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
        
        if piece.type == 'queen':
            print("Generating queen moves")
            return self.generate_queen_moves(position, piece.color)
        
        if piece.type == 'king':
            print("Generating king moves")
            return self.generate_king_moves(position, piece.color)

board = Board()
board.setup_from_FEN("rnbqk2r/pppp1ppp/5n2/2b1p3/2B1P3/5N2/PPPP1PPP/RNBQ1RK1 b kq - 5 4")
board.print_board()
moves = board.generate_moves(60)
print(moves)
print(board.make_move(moves[-1]))
board.print_board()

print(board.undo_move())
board.print_board()