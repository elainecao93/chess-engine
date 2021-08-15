from classes.moves import Move
from classes.pieces import PieceType, PieceColor, Piece

class BoardPosition():
    def __init__(self, pieces, to_move):
        self.board = [[None for x in range(0, 8)] for y in range(0, 8)]
        for piece in pieces:
            self.board[piece.position_file][piece.position_rank] = piece
        self.to_move = to_move

    def __str__(self):
        print("".join(["-" for _ in range(0, 33)]))
        for row in reversed(self.board):
            print("|" + "|".join([k.__repr__() if k else "'-'" for k in row]) + "|")
            print("".join(["-" for _ in range(0, 33)]))


def test():
    testPiece = Piece("e4", PieceColor.WHITE, PieceType.KING)
    blah = BoardPosition([testPiece])
    for row in reversed(blah.board):
        print(["-" if x == None else x for x in row])


if __name__ == "__main__":
    test()