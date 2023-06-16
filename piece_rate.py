 # Positional score values for each piece

PAWN_TABLE = [
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10, -30, -30, 10, 10,  5,
    5, -5, -10,  0,  0, -10, -5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5,  5, 10, 25, 25, 10,  5,  5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0,  0,  0,  0,  0,  0,  0,  0
]

KNIGHT_TABLE = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 15, 20, 20, 15, 0, -30,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50
]

BISHOP_TABLE = [
    -20, -10, -20, -10, -10, -20, -10, -20,
    -10, 10, 0, 0, 0, 0, 10, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20
]

ROOK_TABLE = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 5, 5, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0
]

QUEEN_TABLE = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 5, 0, 0, 0, 0, -10,
    -10, 5, 5, 5, 5, 5, 0, -10,
    0, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20
]

def calculate_piece_position_score(board, category , position_table):
    # Calculate the positional score for a specific category of pieces on the board.
    white_score = 0
    black_score = 0

    for i in range(64):
        x, y = divmod(i, 8)
        piece = board.position[x][y]
        if piece and piece.category  == category :
            if piece.color == "W":
                white_score += position_table[i]
            else:
                black_score += position_table[63 - i]

    return white_score - black_score


def calculate_total_exchange(board):
    # Calculate the total material exchange score on the board.
    white_exchange = 0
    black_exchange = 0

    for x in range(8):
        for y in range(8):
            piece = board.position[x][y]
            if piece:
                if piece.color == "W":
                    white_exchange += piece.relative_value
                else:
                    black_exchange += piece.relative_value

    return white_exchange - black_exchange

def chessboard_evaluation(board):
    # Evaluate the overall score of the chessboard.
    pieces_types = ["P", "N", "B", "R", "Q"]
    pieces_tables = [PAWN_TABLE, KNIGHT_TABLE, BISHOP_TABLE, ROOK_TABLE, QUEEN_TABLE]
    scores = [calculate_piece_position_score(board, piece_type, table) for piece_type, table in zip(pieces_types,pieces_tables )]
    total_score = calculate_total_exchange(board) + sum(scores)
    return total_score


