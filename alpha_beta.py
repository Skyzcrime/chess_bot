import board, piece_rate

MAX_SCORE = 9999
MIN_SCORE = -9999

def alphabeta(chessboard, depth, alpha, beta, is_max):
    # Perform Alpha-Beta Pruning algorithm to evaluate the best move 
    if (depth == 0):
        return piece_rate.chessboard_evaluation(chessboard)

    if is_max:
        best_score = MIN_SCORE
        for action in chessboard.all_actions_on_list("W"):
            copy = board.Board.copy(chessboard)
            copy.perform_action(action)

            best_score = max(best_score, alphabeta(copy, depth-1, alpha, beta, False))
            alpha = max(alpha, best_score)
            if (beta <= alpha):
                break
        return best_score
    else:
        best_score = MAX_SCORE
        for action in chessboard.all_actions_on_list("B"):
            copy = board.Board.copy(chessboard)
            copy.perform_action(action)

            best_score = min(best_score, alphabeta(copy, depth-1, alpha, beta, True))
            beta = min(beta, best_score)
            if (beta <= alpha):
                break
        return best_score