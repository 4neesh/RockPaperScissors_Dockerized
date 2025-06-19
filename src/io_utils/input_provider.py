from abc import ABC, abstractmethod


class InputProvider(ABC):
    """
    Abstract base class for input providers that handle user input during the game.
    Specific input methods (console, GUI, etc.) should inherit from this class and implement
    the abstract methods for requesting various types of input.
    """
    @abstractmethod
    def player_name_request(self, player_id: int) -> str:
        pass

    @abstractmethod
    def play_again_request(self) -> str:
        pass

    @abstractmethod
    def player_rps_request(self, player_id: int, choices: str, time_limit: int = None) -> str:
        """
        Request a player's move in the rock-paper-scissors game.
        
        Args:
            player_id: The ID of the player making the move
            choices: The available choices for the player
            time_limit: Optional time limit in seconds for making the move
            
        Returns:
            The player's move as a string, or None/empty string if timed out
        """
        pass

    @abstractmethod
    def rounds_of_game_request(self, max_rounds: int) -> str:
        pass

    @abstractmethod
    def game_mode_request(self) -> str:
        pass
