import signal
from src.game_utils.game_mode import GameMode
from src.io_utils.input_provider import InputProvider
from constants import Messages, Timeouts, GameConfig


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
        return input(Messages.GAME_MODE_PROMPT.format(
            modes=', '.join(GameMode.formatted_choices())
        )).strip()

    def player_name_request(self, player_id: int) -> str:
        return input(Messages.PLAYER_NAME_PROMPT.format(player_id=player_id)).strip()

    def play_again_request(self) -> str:
        return input(Messages.PLAY_AGAIN_PROMPT).strip()

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
        if time_limit:
            prompt = Messages.MOVE_PROMPT_WITH_TIME.format(
                player_id=player_id,
                choices=choices,
                exit_cmd=GameConfig.EXIT_COMMAND,
                time_limit=time_limit
            ) + "\n"
        else:
            prompt = Messages.MOVE_PROMPT.format(
                player_id=player_id,
                choices=choices,
                exit_cmd=GameConfig.EXIT_COMMAND
            ) + "\n"

        # If no time limit, just use regular input
        if not time_limit:
            return input(prompt).strip()

        # Set up the timeout handler
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(time_limit)

        try:
            user_input = input(prompt).strip()
            # Cancel the alarm if input received
            signal.alarm(Timeouts.DEFAULT_ALARM_SIGNAL)
            return user_input
        except TimeoutException:
            # If timeout occurred, return empty string
            print(Messages.TIMEOUT_MESSAGE)
            signal.alarm(Timeouts.DEFAULT_ALARM_SIGNAL)  # Cancel the alarm
            return ""
        finally:
            # Ensure alarm is canceled
            signal.alarm(Timeouts.DEFAULT_ALARM_SIGNAL)

    def rounds_of_game_request(self, max_rounds: int) -> str:
        return input(Messages.ROUNDS_REQUEST_PROMPT.format(max_rounds=max_rounds)).strip()