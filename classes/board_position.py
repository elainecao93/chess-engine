from classes.moves import Move
from classes.pieces import PieceType, PieceColor, Piece
from json import dumps

def evaluate_piece(piece_type):
    if piece_type == PieceType.PAWN:
        return 1
    if piece_type == PieceType.BISHOP or piece_type == PieceType.KNIGHT:
        return 3
    if piece_type == PieceType.ROOK:
        return 5
    if piece_type == PieceType.QUEEN:
        return 9
    return 999

class BoardPosition():
    def __init__(self, pieces, to_move, white_can_castle_kingside = False, white_can_castle_queenside = False, black_can_castle_kingside = False, black_can_castle_queenside = False):
        self.pieces = sorted(pieces, key=lambda p: p.position_rank*10+p.position_file)
        self.to_move = to_move
        self.white_can_castle_kingside = white_can_castle_kingside
        self.white_can_castle_queenside = white_can_castle_queenside
        self.black_can_castle_kingside = black_can_castle_kingside
        self.black_can_castle_queenside = black_can_castle_queenside

    def __str__(self):
        board = [[None for x in range(0, 8)] for y in range(0, 8)]
        for piece in self.pieces:
            board[piece.position_file][piece.position_rank] = piece
        output_rows = ["".join(["-" for _ in range(0, 33)])]
        for row in reversed(board):
            output_rows.append("|" + "|".join(["'" + k.get_piece_identifier() + "'" if k else "'-'" for k in row]) + "|")
            output_rows.append("".join(["-" for _ in range(0, 33)]))
        return "\n".join(output_rows)
    
    def __hash__(self):
        return hash(("".join(self.pieces.__repr__()), self.to_move, self.white_can_castle_kingside, self.white_can_castle_queenside, self.black_can_castle_kingside, self.black_can_castle_queenside))

    def __eq__(self, other):
        return all([x in other.pieces for x in self.pieces]) and self.to_move == other.to_move

    def create_new_position(self, move):
        new_pieces = []
        for piece in self.pieces:
            if piece.position_rank == move.start_rank and piece.position_file == move.start_file:
                new_pieces.append(piece.move_piece(move))
            elif piece.position_rank != move.end_rank or piece.position_file != move.end_file:
                new_pieces.append(piece)
        return BoardPosition(new_pieces, PieceColor.WHITE if self.to_move == PieceColor.BLACK else PieceColor.BLACK)

    def evaluate_position(self):
        base_evaluation = sum([(evaluate_piece(p.piece_type) if p.piece_color == PieceColor.WHITE else -1 * (evaluate_piece(p.piece_type))) for p in self.pieces])
        return base_evaluation


def set_up_starting_position():
    white_pawns = [Piece(PieceColor.WHITE, PieceType.PAWN, position = chr(ord("a")+i)+"2") for i in range(0, 8)]
    black_pawns = [Piece(PieceColor.BLACK, PieceType.PAWN, position = chr(ord("a")+i)+"7") for i in range(0, 8)]
    white_rooks = [Piece(PieceColor.WHITE, PieceType.ROOK, position = square) for square in ["a1", "h1"]]
    black_rooks = [Piece(PieceColor.BLACK, PieceType.ROOK, position = square) for square in ["a8", "h8"]]
    white_knights = [Piece(PieceColor.WHITE, PieceType.KNIGHT, position = square) for square in ["b1", "g1"]]
    black_knights = [Piece(PieceColor.BLACK, PieceType.KNIGHT, position = square) for square in ["b8", "g8"]]
    white_bishops = [Piece(PieceColor.WHITE, PieceType.BISHOP, position = square) for square in ["c1", "f1"]]
    black_bishops = [Piece(PieceColor.BLACK, PieceType.BISHOP, position = square) for square in ["c8", "f8"]]
    white_majors = [Piece(PieceColor.WHITE, i[1], position = i[0]) for i in [("d1", PieceType.QUEEN), ("e1", PieceType.KING)]]
    black_majors = [Piece(PieceColor.BLACK, i[1], position = i[0]) for i in [("d8", PieceType.QUEEN), ("e8", PieceType.KING)]]
    pieces = (white_pawns + black_pawns + white_rooks + black_rooks + white_knights + black_knights + white_bishops + black_bishops + white_majors + black_majors)
    return BoardPosition(pieces, PieceColor.WHITE, True, True, True, True)


if __name__ == "__main__":
    test()