import board, players

def choose_color():
    while True:
        user_choice = input("Choose the color you want to play (B for Black, W for White): ").upper()
        if user_choice == "B":
            return "B"
        elif user_choice == "W":
            return "W"
        else:
            print("Invalid choice. Please enter 'B' for Black or 'W' for White.")


user_color = choose_color()

board = board.Board.new(user_color)
print(board.representation(user_color))

# Déterminer la couleur de l'IA en fonction de l'utilisateur
opponent_color = "W" if user_color == "B" else "B"

GLOBAL = "W"
COUNT = 0

while True:
    print(COUNT)
    COUNT += 1 
    if board.is_check == 404:
        print("Where is my KING ?")
        break
    elif user_color == "B":
        # Vérifier si c'est l'échec et mat pour l'utilisateur
        if board.is_checkmate(user_color):
            print("Checkmate, nice try AI ")
            break

        # Vérifier si c'est l'échec et mat pour l'IA
        if board.is_checkmate(opponent_color):
            print("Checkmate, tremendous AI ")
            break
    
    else:
        if board.is_checkmate(user_color):
            print("Checkmate, tremendous AI ")
            break

        # Vérifier si c'est l'échec et mat pour l'IA
        if board.is_checkmate(opponent_color):
            print("Checkmate, nice try AI ")
            break
        

    if user_color == GLOBAL:
        action = players.verification_player_action(board,user_color)
        board.perform_action(action, user_color)
        print("Your action: " + action.representation(user_color))
        print(board.representation(user_color))
    else:
        invalid_actions = []
        ai_action = players.get_ai_action(board, invalid_actions, COUNT, user_color)
        if ai_action == 0:
            if board.is_check(opponent_color):
                print("Checkmate, nice try AI ")
            else:
                print("Stalemate :(")
            break

        board.perform_action(ai_action, user_color)
        print("AI decides to play: " + ai_action.representation(user_color))
        print(board.representation(user_color))

    if GLOBAL == "W":
        GLOBAL = "B"
    else:
        GLOBAL = "W"