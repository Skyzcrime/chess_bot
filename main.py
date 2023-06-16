import board, players

# Here is th em ain to simulate a game between Bot Zvarri(Black) and you (White)
board = board.Board.new()
print(board.representation())

while True:
    if board.is_check == 404:
        print("WHERE IS THE KING")
        break
    if board.is_checkmate("W"):
        print("Checkmate ! This AI is too good")
        break
    
    action = players.verification_player_action(board)
    board.perform_action(action)
    print("Your action: " + action.representation())
    print(board.representation())
    invalid_actions = []
    ai_action = players.get_ai_action(board, invalid_actions)
    if ai_action == 0:
        if board.is_check("B"):
            print("Checkmate ! Nice try AI")
        else:
            print("Stalemate :( ")
        break

    board.perform_action(ai_action)
    print("AI chooses to play: " + ai_action.representation())
    print(board.representation())

    if board.is_checkmate("B"):
        print("Checkmate ! Nice try AI ")
        break
