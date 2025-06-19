import signal
from src.game_utils.game_mode import GameMode
from src.io_utils.input_provider import InputProvider


class TimeoutException(Exception):
    """Exception raised when a timeout occurs during input."""
    pass


def timeout_handler(signum, frame):
    """Handler for timeout signal."""
    raise TimeoutException()


class InputProviderConsole(InputProvider):
    """
    An implementation of the InputProvider class that handles user input 
    via the console.
    """
    def game_mode_request(self) -> str:
        return input(f"Please enter a number to select a game mode: {', '.join(GameMode.formatted_choices())} \n").strip()

    def player_name_request(self, player_id: int) -> str:
        return input(f"Please enter player {player_id} name: ").strip()

    def play_again_request(self) -> str:
        return input("\nEnter 'y' to replay, or any key to exit \n").strip()

    def player_rps_request(self, player_id, choices, time_limit: int = None) -> str:
        """
        Request a player's move with an optional time limit.
        
        Args:
            player_id: The ID of the player making the move
            choices: The available choices
            time_limit: Time limit in seconds (None for no limit)
            
        Returns:
            The player's input, or an empty string if timed out
        """
        prompt = f"Player {player_id}: Enter your move ({choices}), or enter 'e' to exit the game"
        if time_limit:
            prompt += f" - You have {time_limit} seconds to respond"
        prompt += "\n"
        
        # If no time limit, just use regular input
        if not time_limit:
            return input(prompt).strip()
            
        # Set up the timeout handler
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(time_limit)
        
        try:
            user_input = input(prompt).strip()
            # Cancel the alarm if input received
            signal.alarm(0)
            return user_input
        except TimeoutException:
            # If timeout occurred, return empty string
            print(f"\nTime's up!")
            signal.alarm(0)  # Cancel the alarm
            return ""
        finally:
            # Ensure alarm is canceled
            signal.alarm(0)

    def rounds_of_game_request(self, max_rounds: int) -> str:
        return input(f"How many rounds of Rock, Paper, Scissors would you like to play? (Max: {max_rounds}) \n").strip()