class ChessAction:
    def __init__(self, source_x, source_y, destination_x, destination_y, en_passant=False):
        # Initializes a ChessAction object with source and destination coordinates and en_passant flag.
        self.source_x = source_x
        self.source_y = source_y
        self.destination_x = destination_x
        self.destination_y = destination_y
        self.en_passant = en_passant

    def representation(self, user_color):
        # Returns a string representation of the action in the format "source_square to destination_square".
        if user_color == "B":
            # Invert the coordinates for the Black's perspective
            source_square = chr(ord('H') - self.source_x) + str(self.source_y + 1)
            destination_square = chr(ord('H') - self.destination_x) + str(self.destination_y + 1)
        else:
            source_square = chr(ord('A') + self.source_x) + str(8 - self.source_y)
            destination_square = chr(ord('A') + self.destination_x) + str(8 - self.destination_y)

        return source_square + " to " + destination_square


    def is_invalid_action(self, invalid_actions):
        # Checks if the current action is in the list of invalid actions.
        for invalid_action in invalid_actions:
            if invalid_action.is_same_to(self):
                return True
        return False

    def is_same_to(self, other_action):
        # Checks if the current action is the same as another action.
        return (
            self.source_x == other_action.source_x
            and self.source_y == other_action.source_y
            and self.destination_x == other_action.destination_x
            and self.destination_y == other_action.destination_y
            and self.en_passant == other_action.en_passant
        )

        
