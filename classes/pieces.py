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
    def __init__(self, piece_color, piece_type, position=None, position_rank=None, position_file=None):
        self.piece_color = piece_color
        self.piece_type = piece_type
        if not position:
            self.position_rank = position_rank
            self.position_file = position_file
        else:
            self.position_rank = ord(position[0])-ord('a')
            self.position_file = int(position[1])-1

    def get_piece_identifier(self):
        identifier = "N" if self.piece_type == PieceType.KNIGHT else self.piece_type.name[0]
        return identifier.upper() if self.piece_color == PieceColor.WHITE else identifier.lower()

    def __repr__(self):
        piece_identifier = "'" + self.get_piece_identifier()
        return piece_identifier + str(self.position_rank) + str(self.position_file)  + "'"

    def __hash__(self):
        return hash((self.piece_color, self.piece_type, self.position_file, self.position_rank))
    
    def __eq__(self, other):
        return (self.piece_color, self.piece_type, self.position_file, self.position_rank) == (other.piece_color, other.piece_type, other.position_file, other.position_rank)

    def move_piece(self, move):
        if self.position_rank != move.start_rank or self.position_file != move.start_file or self.piece_color != move.piece_color or self.piece_type != move.piece_type:
            print(f"error moving {self} with {move}")
            return
        return Piece(self.piece_color, self.piece_type, position_rank = move.end_rank, position_file = move.end_file)
