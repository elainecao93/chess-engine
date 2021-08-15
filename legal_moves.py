from classes.board_position import BoardPosition
from classes.moves import Move
from classes.pieces import PieceType, PieceColor, Piece
from enum import Enum

class MoveDirection(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    UP_LEFT = 5
    UP_RIGHT = 6
    DOWN_LEFT = 7
    DOWN_RIGHT = 8


class MoveAbility(Enum):
    CAN_MOVE = 1
    CAN_CAPTURE = 2
    BLOCKED = 3


ALLOWED_KNIGHT_MOVEMENT = [(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]
ALLOWED_KING_MOVEMENT = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
PAWN_CAPTURE_WHITE = [(1, 1), (-1, 1)]
PAWN_CAPTURE_BLACK = [(1, -1), (-1, -1)]


def get_legal_moves(position):
    owned_pieces = []
    for row in position.board:
        for square in row:
            if square != None and square.piece_color == position.to_move:
                owned_pieces.append(square)
    moves = []
    for piece in owned_pieces:
        allowed_squares = []
        if piece.piece_type == PieceType.ROOK:
            allowed_squares = get_straight_moves(position, (piece.position_rank, piece.position_file), piece.piece_color)
        if piece.piece_type == PieceType.BISHOP:
            allowed_squares = get_diagonal_moves(position, (piece.position_rank, piece.position_file), piece.piece_color)
        if piece.piece_type == PieceType.QUEEN:
            allowed_squares = get_diagonal_moves(position, (piece.position_rank, piece.position_file), piece.piece_color) + get_straight_moves(position, (piece.position_rank, piece.position_file), piece.piece_color)
        if piece.piece_type == PieceType.KNIGHT:
            allowed_squares = get_discrete_moves(position, (piece.position_rank, piece.position_file), piece.piece_color, ALLOWED_KNIGHT_MOVEMENT)
        if piece.piece_type == PieceType.KING:
            allowed_squares = get_discrete_moves(position, (piece.position_rank, piece.position_file), piece.piece_color, ALLOWED_KING_MOVEMENT)
        if piece.piece_type == PieceType.PAWN:
            allowed_squares = get_pawn_moves(position, (piece.position_rank, piece.position_file), piece.piece_color)
        moves = ([Move(piece.position_rank, piece.position_file, square[0], square[1], piece.piece_type, piece.piece_color) for square in allowed_squares]) + moves
    print(moves)


def get_diagonal_moves(position, square, piece_color):
    moves_up_left = move_in_direction(position, MoveDirection.UP_LEFT, get_next_square(square, MoveDirection.UP_LEFT), piece_color)
    moves_up_right = move_in_direction(position, MoveDirection.UP_RIGHT, get_next_square(square, MoveDirection.UP_RIGHT), piece_color)
    moves_down_left = move_in_direction(position, MoveDirection.DOWN_LEFT, get_next_square(square, MoveDirection.DOWN_LEFT), piece_color)
    moves_down_right = move_in_direction(position, MoveDirection.DOWN_RIGHT, get_next_square(square, MoveDirection.DOWN_RIGHT), piece_color)
    return moves_up_left + moves_up_right + moves_down_left + moves_down_right


def get_straight_moves(position, square, piece_color):
    moves_up = move_in_direction(position, MoveDirection.UP, get_next_square(square, MoveDirection.UP), piece_color)
    moves_down = move_in_direction(position, MoveDirection.DOWN, get_next_square(square, MoveDirection.DOWN), piece_color)
    moves_left = move_in_direction(position, MoveDirection.LEFT, get_next_square(square, MoveDirection.LEFT), piece_color)
    moves_right = move_in_direction(position, MoveDirection.RIGHT, get_next_square(square, MoveDirection.RIGHT), piece_color)
    return moves_up + moves_down + moves_left + moves_right


def move_in_direction(position, move_direction, square, piece_color):
    square_allowance = is_square_blocked(position, square, piece_color)
    if square_allowance == MoveAbility.BLOCKED:
        return []
    if square_allowance == MoveAbility.CAN_CAPTURE:
        return [square]
    if square_allowance == MoveAbility.CAN_MOVE:
        allowed_squares = move_in_direction(position, move_direction, get_next_square(square, move_direction), piece_color)
        allowed_squares.append(square)
        return allowed_squares


def get_discrete_moves(position, square, piece_color, move_indices):
    return [(square[0]+i[0], square[1]+i[1]) for i in move_indices if (k := is_square_blocked(position, (square[0]+i[0], square[1]+i[1]), piece_color) != MoveAbility.BLOCKED)]


def get_pawn_moves(position, square, piece_color):
    if piece_color == PieceColor.WHITE:
        captures = [(square[0]+i[0], square[1]+i[1]) for i in PAWN_CAPTURE_WHITE if (k := is_square_blocked(position, (square[0]+i[0], square[1]+i[1]), piece_color) == MoveAbility.CAN_CAPTURE)]
        movement = [(square[0]+i[0], square[1]+i[1]) for i in ([(0, 1), (0, 2)] if square[1] == 1 else [(0, 1)]) if (k := is_square_blocked(position, (square[0]+i[0], square[1]+i[1]), piece_color) == MoveAbility.CAN_MOVE)]
        return captures + movement
    else:
        captures = [(square[0]+i[0], square[1]+i[1]) for i in PAWN_CAPTURE_BLACK if (k := is_square_blocked(position, (square[0]+i[0], square[1]+i[1]), piece_color) == MoveAbility.CAN_CAPTURE)]
        movement = [(square[0]+i[0], square[1]+i[1]) for i in ([(0, -1), (0, -2)] if square[1] == 1 else [(0, -1)]) if (k := is_square_blocked(position, (square[0]+i[0], square[1]+i[1]), piece_color) == MoveAbility.CAN_MOVE)]
        return captures + movement


def is_square_blocked(position, square, piece_color):
    if square[0] < 0 or square[0] > 7 or square[1] < 0 or square[1] > 7:
        return MoveAbility.BLOCKED
    if position.board[square[1]][square[0]] == None:
        return MoveAbility.CAN_MOVE
    return MoveAbility.CAN_CAPTURE if (position.board[square[1]][square[0]].piece_color != piece_color) else MoveAbility.BLOCKED


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


def test():
    white_rook = Piece("e1", PieceColor.WHITE, PieceType.ROOK)
    white_bishop = Piece("c3", PieceColor.WHITE, PieceType.BISHOP)
    white_knight = Piece("d3", PieceColor.WHITE, PieceType.KNIGHT)
    white_pawn = Piece("g2", PieceColor.WHITE, PieceType.PAWN)
    white_second_pawn = Piece("f4", PieceColor.WHITE, PieceType.PAWN)
    black_piece = Piece("e5", PieceColor.BLACK, PieceType.ROOK)
    position = BoardPosition([white_rook, white_bishop, white_knight, white_pawn, white_second_pawn, black_piece], PieceColor.WHITE)
    print(position.__str__())
    output = get_legal_moves(position)


if __name__ == "__main__":
    test()
