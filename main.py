from classes.board_position import BoardPosition, set_up_starting_position
from classes.moves import Move
from classes.pieces import PieceType, PieceColor, Piece
from legal_moves import get_legal_moves


def main():
    board = set_up_starting_position()
    print(board)
    print(board.evaluate_position())
    print(get_legal_moves(board))
    print(board.pieces)
    print("".join([piece.__repr__() for piece in board.pieces]))
    print(hash("".join([piece.__repr__() for piece in board.pieces])))
    print(hash(board))

    second_board = set_up_starting_position()
    print("".join([piece.__repr__() for piece in second_board.pieces]))
    print(hash("".join([piece.__repr__() for piece in second_board.pieces])))
    print(hash(board))



if __name__ == "__main__":
    main()