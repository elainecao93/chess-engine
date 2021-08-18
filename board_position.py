from classes.moves import Move
from classes.pieces import PieceType, PieceColor, Piece
from classes.move_enums import MoveDirection, MoveAbility
from json import dumps

ALLOWED_KNIGHT_MOVEMENT = [(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]
ALLOWED_KING_MOVEMENT = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
PAWN_CAPTURE_WHITE = [(1, 1), (-1, 1)]
PAWN_CAPTURE_BLACK = [(1, -1), (-1, -1)]

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

    def get_legal_moves(self):
        owned_pieces = []
        for piece in self.pieces:
            if piece.piece_color == self.to_move:
                owned_pieces.append(piece)
        moves = []
        for piece in owned_pieces:
            allowed_squares = []
            if piece.piece_type == PieceType.ROOK:
                allowed_squares = self.get_straight_moves((piece.position_rank, piece.position_file), piece.piece_color)
            if piece.piece_type == PieceType.BISHOP:
                allowed_squares = self.get_diagonal_moves((piece.position_rank, piece.position_file), piece.piece_color)
            if piece.piece_type == PieceType.QUEEN:
                allowed_squares = self.get_diagonal_moves((piece.position_rank, piece.position_file), piece.piece_color) + self.get_straight_moves((piece.position_rank, piece.position_file), piece.piece_color)
            if piece.piece_type == PieceType.KNIGHT:
                allowed_squares = self.get_discrete_moves((piece.position_rank, piece.position_file), piece.piece_color, ALLOWED_KNIGHT_MOVEMENT)
            if piece.piece_type == PieceType.KING:
                allowed_squares = self.get_discrete_moves((piece.position_rank, piece.position_file), piece.piece_color, ALLOWED_KING_MOVEMENT)
            if piece.piece_type == PieceType.PAWN:
                allowed_squares = self.get_pawn_moves((piece.position_rank, piece.position_file), piece.piece_color)
            moves = ([Move(piece.position_rank, piece.position_file, square[0], square[1], piece.piece_type, piece.piece_color) for square in allowed_squares]) + moves
        return moves

    def get_diagonal_moves(self, square, piece_color):
        moves_up_left = self.move_in_direction(MoveDirection.UP_LEFT, get_next_square(square, MoveDirection.UP_LEFT), piece_color)
        moves_up_right = self.move_in_direction(MoveDirection.UP_RIGHT, get_next_square(square, MoveDirection.UP_RIGHT), piece_color)
        moves_down_left = self.move_in_direction(MoveDirection.DOWN_LEFT, get_next_square(square, MoveDirection.DOWN_LEFT), piece_color)
        moves_down_right = self.move_in_direction(MoveDirection.DOWN_RIGHT, get_next_square(square, MoveDirection.DOWN_RIGHT), piece_color)
        return moves_up_left + moves_up_right + moves_down_left + moves_down_right

    def get_straight_moves(self, square, piece_color):
        moves_up = self.move_in_direction(MoveDirection.UP, get_next_square(square, MoveDirection.UP), piece_color)
        moves_down = self.move_in_direction(MoveDirection.DOWN, get_next_square(square, MoveDirection.DOWN), piece_color)
        moves_left = self.move_in_direction(MoveDirection.LEFT, get_next_square(square, MoveDirection.LEFT), piece_color)
        moves_right = self.move_in_direction(MoveDirection.RIGHT, get_next_square(square, MoveDirection.RIGHT), piece_color)
        return moves_up + moves_down + moves_left + moves_right

    def move_in_direction(self, move_direction, square, piece_color):
        square_allowance = self.is_square_blocked(square, piece_color)
        if square_allowance == MoveAbility.BLOCKED:
            return []
        if square_allowance == MoveAbility.CAN_CAPTURE:
            return [square]
        if square_allowance == MoveAbility.CAN_MOVE:
            allowed_squares = self.move_in_direction(move_direction, get_next_square(square, move_direction), piece_color)
            allowed_squares.append(square)
            return allowed_squares

    def get_discrete_moves(self, square, piece_color, move_indices):
        return [(square[0]+i[0], square[1]+i[1]) for i in move_indices if (k := self.is_square_blocked((square[0]+i[0], square[1]+i[1]), piece_color) != MoveAbility.BLOCKED)]

    def get_pawn_moves(self, square, piece_color):
        if piece_color == PieceColor.WHITE:
            captures = [(square[0]+i[0], square[1]+i[1]) for i in PAWN_CAPTURE_WHITE if (k := self.is_square_blocked((square[0]+i[0], square[1]+i[1]), piece_color) == MoveAbility.CAN_CAPTURE)]
            movement = [(square[0]+i[0], square[1]+i[1]) for i in ([(0, 1), (0, 2)] if square[1] == 1 else [(0, 1)]) if (k := self.is_square_blocked((square[0]+i[0], square[1]+i[1]), piece_color) == MoveAbility.CAN_MOVE)]
            return captures + movement
        else:
            captures = [(square[0]+i[0], square[1]+i[1]) for i in PAWN_CAPTURE_BLACK if (k := self.is_square_blocked((square[0]+i[0], square[1]+i[1]), piece_color) == MoveAbility.CAN_CAPTURE)]
            movement = [(square[0]+i[0], square[1]+i[1]) for i in ([(0, -1), (0, -2)] if square[1] == 1 else [(0, -1)]) if (k := self.is_square_blocked((square[0]+i[0], square[1]+i[1]), piece_color) == MoveAbility.CAN_MOVE)]
            return captures + movement

    def is_square_blocked(self, square, piece_color):
        if square[0] < 0 or square[0] > 7 or square[1] < 0 or square[1] > 7:
            return MoveAbility.BLOCKED
        pieces_on_square = [piece for piece in self.pieces if piece.position_file == square[1] and piece.position_rank == square[0]]
        if len(pieces_on_square) == 0:
            return MoveAbility.CAN_MOVE
        return MoveAbility.CAN_CAPTURE if (pieces_on_square[0].piece_color != piece_color) else MoveAbility.BLOCKED


def get_next_square(origin_square, move_direction):
    if move_direction == MoveDirection.UP:
        return (origin_square[0], origin_square[1]+1)
    if move_direction == MoveDirection.DOWN:
        return (origin_square[0], origin_square[1]-1)
    if move_direction == MoveDirection.LEFT:
        return (origin_square[0]-1, origin_square[1])
    if move_direction == MoveDirection.RIGHT:
        return (origin_square[0]+1, origin_square[1])
    if move_direction == MoveDirection.UP_LEFT:
        return (origin_square[0]-1, origin_square[1]+1)
    if move_direction == MoveDirection.UP_RIGHT:
        return (origin_square[0]+1, origin_square[1]+1)
    if move_direction == MoveDirection.DOWN_LEFT:
        return (origin_square[0]-1, origin_square[1]-1)
    if move_direction == MoveDirection.DOWN_RIGHT:
        return (origin_square[0]+1, origin_square[1]-1)

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

def test():
    white_rook = Piece(PieceColor.WHITE, PieceType.ROOK, position="e1")
    white_bishop = Piece(PieceColor.WHITE, PieceType.BISHOP, position="c3")
    white_knight = Piece(PieceColor.WHITE, PieceType.KNIGHT, position="d3")
    white_pawn = Piece(PieceColor.WHITE, PieceType.PAWN, position="g2")
    white_second_pawn = Piece(PieceColor.WHITE, PieceType.PAWN, position="f4")
    black_piece = Piece(PieceColor.BLACK, PieceType.ROOK, position="e5")
    position = BoardPosition({white_rook, white_bishop, white_knight, white_pawn, white_second_pawn, black_piece}, PieceColor.WHITE)
    print(position)
    print(position.get_legal_moves())


if __name__ == "__main__":
    test()
