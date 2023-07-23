import board
from chess_action import ChessAction
from alpha_beta import alphabeta


# Converts a letter (A-H) to the x position on the chess board.
def convert_alphabet_to_abscissa(letter):
    letter = letter.upper()
    letters = "ABCDEFGH"
    if letter in letters:
        return letters.index(letter)
    raise ValueError("Invalid letter.")

def get_ai_action(chessboard, forbidden_action, count, user_color):
    # Find the best action using the Alpha-Beta algorithm
    best_action = 0
    best_action_value = 9999
    for action in chessboard.all_actions_on_list("B"):
        if action.is_invalid_action(forbidden_action):
            continue

        copy = board.Board.copy(chessboard)
        copy.perform_action(action, user_color)
        if count < 24:
            score = alphabeta(copy, 3, -9999, 9999, "max", user_color)
        else:
            score = alphabeta(copy, 4, -9999, 9999, "max", user_color)
            
        if score < best_action_value:
            best_action_value = score
            best_action = action


    # Checkmate case.
    if best_action == 0:
        return 0
    # En passant case. 
    elif best_action.en_passant : 
        dest_x = best_action.destination_x
        dest_y = best_action.destination_y
        chessboard.position[dest_x][dest_y-1] = 0
        

    copy = board.Board.copy(chessboard)
    copy.perform_action(best_action, user_color)
    if copy.is_check("B"):
        forbidden_action.append(best_action)
        return get_ai_action(chessboard, forbidden_action)

    return best_action

def player_action(user_color):
    # Get the player's action input
    print(" Type: D2 D4  (for example)")
    action_str = input("Your time to shine  ").replace(" ", "")

    try:
        if user_color == "B":
            # Invert the coordinates for the Black's perspective
            source_x = 7 - convert_alphabet_to_abscissa(action_str[0:1])
            source_y = int(action_str[1:2]) - 1
            destination_x = 7 - convert_alphabet_to_abscissa(action_str[2:3])
            destination_y = int(action_str[3:4]) - 1
        else:
            source_x = convert_alphabet_to_abscissa(action_str[0:1])
            source_y = 8 - int(action_str[1:2])
            destination_x = convert_alphabet_to_abscissa(action_str[2:3])
            destination_y = 8 - int(action_str[3:4])

        return ChessAction(source_x, source_y, destination_x, destination_y)
    except ValueError:
        print("You can't do that")
        return player_action(user_color)


def verification_player_action(board, user_color):
    while True:
        # Get the action input from you (the user)
        action = player_action(user_color)

        # Set the action to forbidden 
        forbidden = True
        possible_actions = board.all_actions_on_list("W")
        
        # Iterate over the possible actions to check if the entered action is valid
        for possible_action in possible_actions:
            if action.is_same_to(possible_action):
                forbidden = False
                break
        
        if not forbidden:
            break
        else:
            print("Check the rules of chess")
    
    return action
