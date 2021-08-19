from board_position import BoardPosition, set_up_starting_position
from get_best_move import get_best_move
from classes.moves import Move
from classes.pieces import PieceType, PieceColor, Piece
from time import sleep

def parse_user_move(user_move):
    piece_char = user_move[0]
    starting_square = user_move[1:3]
    ending_square = user_move[3:5]
    print((piece_char, starting_square, ending_square))
    return Move(int(starting_square[1])-1, ord(starting_square[0])-ord('a'), int(ending_square[1])-1, ord(ending_square[0])-ord('a'), PieceType.KING, PieceColor.BLACK)


def main():
    pieces = [Piece(PieceColor.WHITE, PieceType.QUEEN, position="a1"), Piece(PieceColor.WHITE, PieceType.KING, position="e5"), Piece(PieceColor.BLACK, PieceType.KING, position="e8")]
    board = BoardPosition(pieces, PieceColor.WHITE)
    move_count = 0
    while True:
        engine_move = get_best_move(board)[0]
        board = board.create_new_position(engine_move)
        print("*****")
        print("Move count: " + str(move_count))
        print("Computer just moved: " + str(engine_move))
        print(board)
        user_move = parse_user_move(input("Enter move"))
        board = board.create_new_position(user_move)
        move_count = move_count + 1
        print(user_move)
        print(board)
        print(board.pieces)
        sleep(5)


if __name__ == "__main__":
    main()