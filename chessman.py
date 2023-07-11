from chess_action import ChessAction 

class ChessPiece:
    def __init__(self, x, y, color, category, relative_value):
        # Initializes a  Chesspiece with its position, color, category, and relative value.
        self.x = x
        self.y = y
        self.color = color
        self.category = category
        self.relative_value = relative_value

    def get_all_possible_actions(self, board, category):
        # Returns a list of all possible actions for the piece on the given board, based on its category.
        possible_actions = []
        directions = []
        if category == "B" or category == "Q":
            directions += [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        if category == "R" or category == "Q":
            directions += [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for direction in directions:
            dx, dy = direction
            x, y = self.x + dx, self.y + dy

            while board.inside(x, y):
                piece = board.get_piece_at_position(x, y)
                possible_actions.append(self.possible_action(board, x, y))

                if piece:
                    break

                x += dx
                y += dy

        return self.filter_valid_action(possible_actions)

    def possible_action(self, board, destination_x, destination_y, en_passant=False):
        # Determines if a possible action is valid, given the destination coordinates on the board.
        if not board.inside(destination_x, destination_y):
            return None

        destination_piece = board.get_piece_at_position(destination_x, destination_y)
        
        if en_passant:
            # Capture en passant
            return ChessAction(self.x, self.y, destination_x, destination_y, en_passant=True)
        
        if destination_piece and destination_piece.color != self.color:
            return ChessAction(self.x, self.y, destination_x, destination_y)

        if not destination_piece:
            return ChessAction(self.x, self.y, destination_x, destination_y)

        return None


    def filter_valid_action(self, l):
        # Filters out None values from a list of actions.
        return [action for action in l if action]

    def filter_valid_action(self, l):
        return [action for action in l if action]

class Rook(ChessPiece):

    def __init__(self, x, y, color):
        ChessPiece.__init__(self, x, y, color, "R", 500)

    def calculate_valid_actions(self, board):
        return self.get_all_possible_actions(board, "R")

    def piece_copy(self):
        return Rook(self.x, self.y, self.color)


class Knight(ChessPiece):

    def __init__(self, x, y, color):
        ChessPiece.__init__(self, x, y, color, "N", 320)

    def calculate_valid_actions(self, board):
        actions = []

        possible_actions = [(2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (1, 2), (-2, -1), (-1, -2)]

        for dx, dy in possible_actions:
            actions.append(self.possible_action(board, self.x + dx, self.y + dy))

        return self.filter_valid_action(actions)

    def piece_copy(self):
        return Knight(self.x, self.y, self.color)



class Bishop(ChessPiece):

    def __init__(self, x, y, color):
        ChessPiece.__init__(self, x, y, color, "B", 330)

    def calculate_valid_actions(self, board):
        return self.get_all_possible_actions(board, "B")

    def piece_copy(self):
        return Bishop(self.x, self.y, self.color)


class Queen(ChessPiece):

    def __init__(self, x, y, color):
        ChessPiece.__init__(self, x, y, color, "Q", 900)

    def calculate_valid_actions(self, board):
        return self.get_all_possible_actions(board, "Q")

    def piece_copy(self):
        return Queen(self.x, self.y, self.color)


class King(ChessPiece):

    def __init__(self, x, y, color):
        ChessPiece.__init__(self, x, y, color, "K", 25000)

    def kcastle_action(self, board):
        # Checks if the king can perform a kingside castle action by verifying the necessary conditions
        if (self.color == "W" and not board.white_castle) or (self.color == "B" and not board.black_castle):
            return 0
        
        rook = board.get_piece_at_position(self.x + 3, self.y)
        if rook is None or rook == 0 or rook.category != "R" or rook.color != self.color:
            return 0
        
        if any(board.get_piece_at_position(self.x + i, self.y) != 0 for i in range(1, 3)):
            return 0
        
        return ChessAction(self.x, self.y, self.x + 2, self.y)

    def qcastle_action(self, board):
        # Checks if the king can perform a queenside castle action by verifying the necessary conditions
        if (self.color == "W" and not board.white_castle) or (self.color == "B" and not board.black_castle):
            return 0
        
        rook = board.get_piece_at_position(self.x - 4, self.y)
        if rook is None or rook == 0 or rook.category != "R" or rook.color != self.color:
            return 0
        
        if any(board.get_piece_at_position(self.x - i, self.y) != 0 for i in range(1, 4)):
            return 0
        
        return ChessAction(self.x, self.y, self.x - 2, self.y)


    def calculate_valid_actions(self, board):
        actions = [self.kcastle_action(board), self.qcastle_action(board)]
        if not board.is_check :
            actions = []
        directions = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]

        for dx, dy in directions:
            x, y = self.x + dx, self.y + dy
            actions.append(self.possible_action(board, x, y))

 
        return self.filter_valid_action(actions)
    
    def piece_copy(self):
        return King(self.x, self.y, self.color)
    


class Pawn(ChessPiece):


    def __init__(self, x, y, color):
        ChessPiece.__init__(self, x, y, color, "P", 100)
        self.en_passanted_b = False
        self.en_passanted_w = False

    def if_pawn_moved(self):
        if (self.color == "B"):
            return self.y != 1
        else:
            return self.y != 8 - 2

    def calculate_valid_actions(self, board):
        # 3 cases : Capture , 1 step or 2 steps
        actions = []
        
        if self.color == "B":

            if board.get_piece_at_position(self.x, self.y + 1) == 0:
                actions.append(self.possible_action(board, self.x, self.y + 1))

            if not self.if_pawn_moved():
                if board.get_piece_at_position(self.x, self.y + 1) == 0:
                    if board.get_piece_at_position(self.x, self.y +  2) == 0:
                        actions.append(self.possible_action(board, self.x, self.y + 2 ))
                        self.en_passanted_b = True

            piece = board.get_piece_at_position(self.x + 1, self.y + 1)
            if piece and piece.color != self.color:
                actions.append(self.possible_action(board, self.x + 1, self.y + 1))

            piece = board.get_piece_at_position(self.x - 1, self.y + 1)
            if piece and piece.color != self.color:
                actions.append(self.possible_action(board, self.x - 1, self.y + 1))

            if self.y == 4:
                # En Passant Verification
                piece = board.get_piece_at_position(self.x - 1, self.y)
                if piece and piece.color != self.color and isinstance(piece, Pawn) and piece.en_passanted_w:
                    actions.append(self.possible_action(board, self.x - 1, self.y + 1, en_passant=True))

                # En Passant Verification
                piece = board.get_piece_at_position(self.x + 1, self.y)
                if piece and piece.color != self.color and isinstance(piece, Pawn) and piece.en_passanted_w:
                    actions.append(self.possible_action(board, self.x + 1, self.y + 1, en_passant=True))



            return self.filter_valid_action(actions)
        
        else:
            if board.get_piece_at_position(self.x, self.y - 1) == 0:
                actions.append(self.possible_action(board, self.x, self.y - 1))

            if not self.if_pawn_moved():
                if board.get_piece_at_position(self.x, self.y - 1) == 0:
                    if board.get_piece_at_position(self.x, self.y - 2) == 0:
                        actions.append(self.possible_action(board, self.x, self.y - 2))
                        self.en_passanted_w = True

            piece = board.get_piece_at_position(self.x + 1, self.y - 1)
            if piece and piece.color != self.color:
                actions.append(self.possible_action(board, self.x + 1, self.y - 1))

            piece = board.get_piece_at_position(self.x - 1, self.y - 1)
            if piece and piece.color != self.color:
                actions.append(self.possible_action(board, self.x - 1, self.y - 1))

            if self.y == 3:
                # En Passant Verification
                piece = board.get_piece_at_position(self.x - 1, self.y)
                if piece and piece.color != self.color and isinstance(piece, Pawn) and piece.en_passanted_b:
                    actions.append(self.possible_action(board, self.x - 1, self.y - 1, en_passant=True))

                # En Passant Verification 
                piece = board.get_piece_at_position(self.x + 1, self.y)
                if piece and piece.color != self.color and isinstance(piece, Pawn) and piece.en_passanted_b:
                    actions.append(self.possible_action(board, self.x + 1, self.y - 1, en_passant=True))
            

            return self.filter_valid_action(actions)




    def piece_copy(self):
        return Pawn(self.x, self.y, self.color)
    
