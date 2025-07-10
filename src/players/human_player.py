from src.game_utils.hand_gesture import HandGesture
from src.players.player import Player
from game import Game


class HumanPlayer(Player):
    """
    Represents a human player in the game. 
    The player provides their name and makes moves interactively.
    """

    def __init__(self, game: Game, player_id: int, time_limit: int = Player.DEFAULT_TIME_LIMIT):
        input_name = ""
        while Player.name_is_invalid(input_name):
            input_name = game.input_provider.player_name_request(player_id)
            if Player.name_is_invalid(input_name):
                game.output_provider.output_name_error()

        super().__init__(input_name, time_limit)
        self._game = game
        self._id = player_id

    def make_move(self) -> HandGesture | None:
        """
        Prompts the player to make a move in the Paper, Scissors, Rock game.
        Continuously requests a valid move from the player until a valid input is provided.
        If no valid move is made within the time limit, returns None to indicate forfeit.
        """
        gesture_options = ", ".join(HandGesture.choices())

        # Request input with time limit
        input_gesture = self._game.input_provider.player_rps_request(
            self._id, gesture_options, self.time_limit
        )

        # Check for timeout (indicated by None or empty string)
        if input_gesture is None or input_gesture == "":
            return None

        # Continue requesting input until valid
        while not self.is_valid_move(input_gesture):
            input_gesture = self._game.input_provider.player_rps_request(
                self._id, gesture_options, self.time_limit
            )
            # Check for timeout again
            if input_gesture is None or input_gesture == "":
                return None

        if input_gesture.isdigit():
            gesture_number = int(input_gesture)
            return HandGesture.get_gesture_by_number(gesture_number)
        elif input_gesture.lower() == self._game.EXIT_COMMAND:
            self._game.exit_game()

    def is_valid_move(self, gesture: str) -> bool:
        """Helper method to validate the move input."""
        if gesture.isdigit():
            gesture_number = int(gesture)
            if HandGesture.validate_entry(gesture_number):
                return True
        elif gesture.lower() == self._game.EXIT_COMMAND:
            return True
        self._game.output_provider.output_gesture_error()
        return False