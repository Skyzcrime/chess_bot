import chessman
from chess_action import ChessAction 
from tabulate import tabulate

class Board:
    
    

    def __init__(self, position, white_castle, black_castle):
        #Initialize the board
        self.position = position
        self.white_castle = white_castle
        self.black_castle = black_castle

    
    def representation(self, user_color):
        # Show the chessboard on the terminal
        headers = [''] + [chr(ord('A') + x) for x in range(8)]
        rows = []

        piece_symbols = {
            'B': {
                'P': '♙', 'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔'
            },
            'W': {
                'P': '♟', 'R': '♜', 'N': '♞', 'B': '♝', 'Q': '♛', 'K': '♚'
            },
        }

        if user_color == "B":
            headers = [''] + [chr(ord('H') - x) for x in range(8)] 
            piece_symbols['B'], piece_symbols['W'] = piece_symbols['W'], piece_symbols['B']

        for y in range(8):
            if user_color == "B":
                row = [str(y+1)]
            else:  
                row = [str(8 - y)]
            for x in range(8 - 1, -1, -1):
                piece = self.position[8 - 1 - x][y]
                if piece != 0:
                    symbol = piece_symbols[piece.color][piece.category]
                    row.append(symbol)
                else:
                    row.append('.')
            rows.append(row)

        table = tabulate(rows, headers=headers, tablefmt='fancy_grid')
        return table


    def inside(self, x, y):
        # Checks if the coordinates (x, y) are inside the board
        return (x >= 0 and y >= 0 and x < 8 and y < 8)
    
    @classmethod
    def copy(cls, chessboard):
        # Creates a copy of the chessboard
        position = [[0 for _ in range(8)] for _ in range(8)]
        for x in range(8):
            for y in range(8):
                piece = chessboard.position[x][y]
                if piece != 0:
                    position[x][y] = piece.piece_copy()
        return cls(position, chessboard.white_castle, chessboard.black_castle)

    @classmethod
    def new(cls, user_color):
    # Creates a new chessboard with initial piece positions. Disclamer ! Whether you play with Black pieces,colours will be upside down due to board.representation
        chess_chessman = [[0 for _ in range(8)] for _ in range(8)]

        piece_positions = [
            (chessman.Pawn, [(x, 8-2) for x in range(8)], "W"),
            (chessman.Pawn, [(x, 1) for x in range(8)], "B"),

            # Rooks
            (chessman.Rook, [(0, 8-1), (8-1, 8-1)], "W"),
            (chessman.Rook, [(0, 0), (8-1, 0)], "B"),

            # Knights
            (chessman.Knight, [(1, 8-1), (8-2, 8-1)], "W"),
            (chessman.Knight, [(1, 0), (8-2, 0)], "B"),

            # Bishops
            (chessman.Bishop, [(2, 8-1), (8-3, 8-1)], "W"),
            (chessman.Bishop, [(2, 0), (8-3, 0)], "B")
        ]
        
        if user_color == "W":
            # King & Queen for White
            piece_positions.extend([
                (chessman.King, [(4, 8-1)], "W"),
                (chessman.Queen, [(3, 8-1)], "W"),
                (chessman.King, [(4, 0)], "B"),
                (chessman.Queen, [(3, 0)], "B") 
            ])
        else:
            # King & Queen for Black
            piece_positions.extend([
                (chessman.King, [(3, 0)], "B"),
                (chessman.Queen, [(4, 0)], "B"),
                (chessman.King, [(3, 8-1)], "W"),
                (chessman.Queen, [(4, 8-1)], "W")  
            ])

        for category, positions, color in piece_positions:
            for position in positions:
                x, y = position
                chess_chessman[x][y] = category(x, y, color)

        return cls(chess_chessman, True, True)


    def find_king(self, color):
        # Finds the position of the king of the specified color on the board
        for x in range(8):
            for y in range(8):
                piece = self.position[x][y]
                if isinstance(piece, chessman.King) and piece.color == color:
                    return (x, y)
        return None

    def is_check(self, color):
        # Checks if the king of the specified color is in check
        king_position = self.find_king(color)
        other_color = "W" if color == "B" else "B"
        for action in self.all_actions_on_list(other_color):
            if king_position is None:
                return 404
            if action.destination_x == king_position[0] and action.destination_y == king_position[1]:
                return True

        return False

    def is_checkmate(self, color):
        # Checks if the king of the specified color is in checkmate
        if not self.is_check(color):
            return False

        possible_actions = self.all_actions_on_list(color)
        for action in possible_actions:
            copy = Board.copy(self)
            copy.perform_action(action, "W")
            if not copy.is_check(color):
                return False

        return True
    
    def get_piece_at_position(self, x, y):
        # Returns the piece at the position (x, y) on the board
        if not self.inside(x, y):
            return None

        return self.position[x][y]


    def action_piece_to_destination(self, piece, x_destination, y_destination):
        # Moves the piece to the specified destination
        if piece != 0 and piece != None:    
            self.position[piece.x][piece.y] = 0
            piece.x = x_destination
            piece.y = y_destination
            self.position[x_destination][y_destination] = piece


    def all_actions_on_list(self, color):
        # Returns a list of all possible actions for the pieces of the specified color on the board
        actions = []
        for x in range(8):
            for y in range(8):
                piece = self.position[x][y]
                if piece != 0 and piece.color == color:
                    actions += piece.calculate_valid_actions(self)

        return actions


    def perform_action(self, action, user_color):
        # Perform an action on the chessboard by moving a piece from a source position to a destination position
        piece = self.position[action.source_x][action.source_y]
        self.action_piece_to_destination(piece, action.destination_x, action.destination_y)

        if isinstance(piece, chessman.Pawn) and (piece.y == 0 or piece.y == 7):
            self.position[piece.x][piece.y] = chessman.Queen(piece.x, piece.y, piece.color)
        if piece.category == "K":
            if piece.color == "W":
                self.white_castle = False
            else:
                self.black_castle = False

            if action.destination_x - action.source_x == 2:
                if user_color == "B":
                    rook = self.position[action.destination_x + 2][action.destination_y]
                    self.action_piece_to_destination(rook, action.destination_x - 1, action.destination_y)
                else:
                    rook = self.position[action.destination_x + 1][action.destination_y]
                    self.action_piece_to_destination(rook, action.destination_x - 1, action.destination_y)
            elif action.destination_x - action.source_x == -2:
                if user_color == "B":
                    rook = self.position[action.destination_x - 1][action.destination_y]
                    self.action_piece_to_destination(rook, action.destination_x + 1, action.destination_y)
                else:
                    rook = self.position[action.destination_x - 2][action.destination_y]
                    self.action_piece_to_destination(rook, action.destination_x + 1, action.destination_y)




   








 


   
    

    
