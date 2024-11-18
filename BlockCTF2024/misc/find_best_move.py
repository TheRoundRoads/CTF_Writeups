import copy

def compress_1d(board):
    new_board = [0] * 16
    for i in range(4):
        pos = i * 4
        for j in range(4):
            if board[i * 4 + j] != 0:
                new_board[pos] = board[i * 4 + j]
                pos += 1
    return new_board

def merge_1d(board):
    merged = False
    for i in range(4):
        for j in range(3):
            if board[i * 4 + j] == board[i * 4 + j + 1] and board[i * 4 + j] != 0:
                board[i * 4 + j] *= 2
                board[i * 4 + j + 1] = 0
                merged = True
    return board, merged

def reverse_1d(board):
    new_board = board[:]
    for i in range(4):
        row_start = i * 4
        new_board[row_start:row_start+4] = board[row_start+3:row_start-1:-1]
    return new_board

def transpose_1d(board):
    new_board = [0] * 16
    for i in range(4):
        for j in range(4):
            new_board[j * 4 + i] = board[i * 4 + j]
    return new_board

def move_left_1d(board):
    new_board = compress_1d(board)
    new_board, merged = merge_1d(new_board)
    new_board = compress_1d(new_board)
    return new_board, merged

def move_right_1d(board):
    new_board = reverse_1d(board)
    new_board, merged = move_left_1d(new_board)
    new_board = reverse_1d(new_board)
    return new_board, merged

def move_up_1d(board):
    new_board = transpose_1d(board)
    new_board, merged = move_left_1d(new_board)
    new_board = transpose_1d(new_board)
    return new_board, merged

def move_down_1d(board):
    new_board = transpose_1d(board)
    new_board, merged = move_right_1d(new_board)
    new_board = transpose_1d(new_board)
    return new_board, merged

# Evaluate board using 1D indexing
def evaluate_board_1d(board):
    empty_cells = board.count(0)
    highest_tile = max(board)
    highest_in_corner = (board[0] == highest_tile or
                         board[3] == highest_tile or
                         board[12] == highest_tile or
                         board[15] == highest_tile)
    
    score = 0
    score += empty_cells * 100       
    score += highest_tile * 10       
    score += 500 if highest_in_corner else 0  

    return score

def find_best_move(board):
    moves = {
        'w': move_up_1d,
        'a': move_left_1d,
        's': move_down_1d,
        'd': move_right_1d
    }
    
    best_move = None
    best_score = -float('inf')
    
    for move_key, move_func in moves.items():
        new_board, merged = move_func(copy.deepcopy(board))
        if new_board != board:  # Valid move check
            score = evaluate_board_1d(new_board)
            if merged:
                score += 200
            if score > best_score:
                best_score = score
                best_move = move_key

    return best_move

if __name__ == "__main__":
    # Example board
    board = [
        2, 0, 2, 4,
        4, 4, 8, 8,
        0, 16, 32, 0,
        2, 0, 0, 2
    ]

    print("Best move:", find_best_move(board))