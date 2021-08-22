from board_position import BoardPosition, set_up_starting_position
from classes.pieces import PieceType, PieceColor, Piece

SEARCH_DEPTH = 50000


def evaluate_recursive(search_list, evaluations, ind, parent_indices):
    if ind in parent_indices:
        return 0 # draw by 3 move rep
    if evaluations[ind]:
        return evaluations[ind]
    to_move = search_list[ind][0].to_move
    if search_list[ind][2]:
        child_evaluations = [evaluate_recursive(search_list, evaluations, child_index, parent_indices + [ind]) for child_index in search_list[ind][2]]
        if to_move == PieceColor.WHITE:
            evaluations[ind] = max(child_evaluations)
            return max(child_evaluations)
        else:
            evaluations[ind] = min(child_evaluations)
            return min(child_evaluations)
    evaluation = search_list[ind][0].evaluate_position()
    evaluations[ind] = evaluation
    return evaluation


def get_best_move(position):
    # each element has position, link to previous position, and links to all next positions
    search_list = [(position, [], [])]
    iterator = 0
    position_hash = {position: 0}

    while True:
    # for each position in list:
    # get list of all legal moves
        current_position = search_list[iterator][0]
    # for each legal move, generate new position
        legal_moves = current_position.get_legal_moves()
        new_positions = [current_position.create_new_position(move) for move in legal_moves]            
    # for each position, check to see if its already in the list using hash
        if [piece.piece_type == PieceType.KING for piece in current_position.pieces].count(True) == 2: # checks if both kings still exist
            for new_position in new_positions:
                if new_position in position_hash:
                    new_position_index = position_hash[new_position]
                    search_list[new_position_index][1].append(iterator)
                else:
                    search_list.append((new_position, [iterator], []))
                    search_list[iterator][2].append(len(search_list)-1)
                    position_hash[new_position] = len(search_list)-1
    # append position to list
        iterator += 1
        if iterator%1000 == 0:
            print(current_position)
            print(legal_moves)
            print(current_position.evaluate_position())
            print(iterator)
            print(len(search_list))
        if iterator > SEARCH_DEPTH or iterator > len(search_list):
            break
    
    print("Evaluating...")
    # when list is full
    # recursively evaluate positions from end
    # only evaluate if not evaluated based on positions
    # pass evaluation to previous positions and update if needed
    evaluations = [None] * len(search_list) 
    position_evaluation = evaluate_recursive(search_list, evaluations, 0, [])
    print(position_evaluation)
    debug_iterator = 0
    while True:
        current_position_moves = search_list[debug_iterator][0].get_legal_moves()
        print(current_position_moves)
        move_indices = search_list[debug_iterator][2]
        if not move_indices:
            break
        next_evals = [evaluations[ind] for ind in move_indices]
        print(next_evals)
        print(current_position_moves[next_evals.index(position_evaluation)])
        next_move_index = move_indices[next_evals.index(position_evaluation)]
        debug_iterator = next_move_index
    child_moves = search_list[0][0].get_legal_moves()
    child_evaluations = [evaluations[ind] for ind in search_list[0][2]]
    return (child_moves[child_evaluations.index(position_evaluation)], position_evaluation)


def test():
    pieces = [Piece(PieceColor.WHITE, PieceType.ROOK, position="a1"), Piece(PieceColor.WHITE, PieceType.KING, position="e1"), Piece(PieceColor.BLACK, PieceType.KING, position="e8")]
    board = BoardPosition(pieces, PieceColor.WHITE)
    best_move = get_best_move(board)


if __name__ == "__main__":
    test()