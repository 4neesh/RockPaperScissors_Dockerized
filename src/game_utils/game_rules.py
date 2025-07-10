from abc import ABC, abstractmethod
from typing import Any, Dict, List, TypeVar, Generic

T = TypeVar('T')  # Generic type for gestures


class GameRules(Generic[T], ABC):
    """
    Abstract base class for game rules.

    This class defines the interface for implementing rule systems for different games.
    Each rule implementation should determine the winner between two moves and provide
    descriptions of interactions between moves.
    """

    @abstractmethod
    def determine_result(self, move_1: T, move_2: T) -> int:
        """
        Determine the result of a comparison between two moves.

        Args:
            move_1: The first move
            move_2: The second move

        Returns:
            1 if move_1 wins, -1 if move_2 wins, 0 if draw
        """
        pass

    @abstractmethod
    def get_interaction_description(self, move_1: T, move_2: T) -> str:
        """
        Get a description of the interaction between two moves.

        Args:
            move_1: The first move
            move_2: The second move

        Returns:
            A string describing the interaction
        """
        pass

    @abstractmethod
    def get_valid_moves(self) -> list[T]:
        """Return the list of valid moves for the game."""
        pass