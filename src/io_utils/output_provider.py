from abc import ABC, abstractmethod
from src.game_utils.hand_gesture import HandGesture
from src.players.player import Player


class OutputProvider(ABC):
    """
    Abstract class for output providers that handle displaying game information to the user.
    Specific output methods (console, GUI, etc.) should inherit from this class and implement
    the abstract methods for presenting various types of information during the game.
    """

    @abstractmethod
    def output_round_number(self, round_number: int, rounds_in_game: int) -> None:
        pass

    @abstractmethod
    def output_round_moves(self, player_1: Player, player_2: Player, player_1_move: HandGesture,
                           player_2_move: HandGesture) -> None:
        pass

    @abstractmethod
    def introduce_game(self, game: str) -> None:
        pass

    @abstractmethod
    def output_scores_table(self, _scores: dict[str, int]) -> None:
        pass

    @abstractmethod
    def output_rounds_error(self, max_rounds: int) -> None:
        pass

    @abstractmethod
    def output_gesture_error(self) -> None:
        pass

    @abstractmethod
    def output_end_game(self) -> None:
        pass

    @abstractmethod
    def output_name_error(self) -> None:
        pass

    @abstractmethod
    def output_round_description(self, description: str) -> None:
        """
        Output the description of a round result.

        Args:
            description: A string describing the round outcome
        """
        pass

    @abstractmethod
    def output_drawn_game(self) -> None:
        pass

    @abstractmethod
    def output_game_winner(self, winner: str, winner_score: int, loser_score: int) -> None:
        pass

    @abstractmethod
    def output_drawn_round(self, player_1_move: str, player_2_move: str) -> None:
        pass

    @abstractmethod
    def output_game_mode_error(self) -> None:
        pass
