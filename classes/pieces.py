from enum import Enum

class PieceType(Enum):
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6


class PieceColor(Enum):
    WHITE = 1
    BLACK = 2


class Piece:
    def __init__(self, position_rank, position_file, piece_color, piece_type):
        self.position_rank = position_rank
        self.position_file = position_file
        self.piece_color = piece_color
        self.piece_type = piece_type


    def __init__(self, position, piece_color, piece_type):
        self.piece_color = piece_color
        self.piece_type = piece_type
        self.position_rank = ord(position[0])-ord('a')
        self.position_file = int(position[1])-1


    def __repr__(self):
        output = "'N'" if self.piece_type == PieceType.KNIGHT else "'" + self.piece_type.name[0] + "'"
        return output.upper() if self.piece_color == PieceColor.WHITE else output.lower()