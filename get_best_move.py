from classes.board_position import BoardPosition, set_up_starting_position
from classes.moves import Move
from classes.pieces import PieceType, PieceColor, Piece
from legal_moves import get_legal_moves

SEARCH_DEPTH = 10000000


def get_depth(iterator, search_list, current_depth = 0):
    if search_list[iterator][1] == 0:
        return 1
    return 1+ get_depth(search_list[iterator][1], search_list)


def get_best_move(position):
    #each element has position, link to previous position, and links to all next positions
    search_list = [(position, None, [])]
    iterator = 0
    position_hash = {position}

    while True:
    #for each position in list:
    #get list of all legal moves
        current_position = search_list[iterator][0]
        legal_moves = get_legal_moves(current_position)
    #for each legal move, generate new position
        new_positions = [current_position.create_new_position(move) for move in legal_moves]
    #for each position, check to see if its already in the list using hash
        for new_position in new_positions:
            if new_position not in position_hash:
                position_hash.add(new_position)
                search_list.append((new_position, iterator, []))
                search_list[iterator][2].append(len(search_list)-1)
    #append position to list
        iterator += 1
        if iterator%1000 == 0:
            print(get_depth(iterator, search_list))
            print(iterator)
            print(current_position)
        if iterator > SEARCH_DEPTH or iterator > len(search_list):
            break

    #when list is full
    #recursively evaluate positions from end
    #only evaluate if not evaluated based on positions
    #pass evaluation to previous positions and update if needed
    pass


def test():
    board = set_up_starting_position()
    print(board)
    get_best_move(board)


if __name__ == "__main__":
    test()