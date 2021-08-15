from classes.pieces import Piece, PieceColor, PieceType

class Move():    
    def __init__(self, start_rank, start_file, end_rank, end_file, piece_type, piece_color, is_capture=False, is_special=False):
        self.start_rank = start_rank
        self.start_file = start_file
        self.end_rank = end_rank
        self.end_file = end_file
        self.piece_type = piece_type
        self.piece_color = piece_color
        self.is_capture = is_capture
        self.is_special = is_special

    def __repr__(self):
        piece_symbol = "N" if self.piece_type == PieceType.KNIGHT else self.piece_type.name[0]
        return piece_symbol + chr(self.end_rank + ord('a')) + str(self.end_file + 1)