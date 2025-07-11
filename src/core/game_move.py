"""
Generic game move interface for extensible game systems.

This module provides a common interface for all game moves, making it easy
to add new game types without modifying the core game logic.
"""

from abc import ABC, abstractmethod
from typing import Any, List


class GameMove(ABC):
    """
    Abstract base class for all game moves.

    This interface allows the game framework to work with any type of move
    (gestures, cards, etc.) without knowing the specific implementation.
    """

    @abstractmethod
    def get_value(self) -> Any:
        """Return the underlying value of this move."""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Return the human-readable name of this move."""
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Return string representation of this move."""
        pass

    @abstractmethod
    def __eq__(self, other) -> bool:
        """Check equality with another move."""
        pass

    @abstractmethod
    def __hash__(self) -> int:
        """Return hash for use in dictionaries."""
        pass

    @classmethod
    @abstractmethod
    def get_all_moves(cls) -> List['GameMove']:
        """Return all valid moves for this game type."""
        pass

    @classmethod
    @abstractmethod
    def get_random_move(cls) -> 'GameMove':
        """Return a random valid move."""
        pass

    @classmethod
    @abstractmethod
    def get_move_by_value(cls, value: Any) -> 'GameMove':
        """Get a move by its value."""
        pass

    @classmethod
    @abstractmethod
    def validate_value(cls, value: Any) -> bool:
        """Validate if a value corresponds to a valid move."""
        pass

    @classmethod
    @abstractmethod
    def get_formatted_choices(cls) -> List[str]:
        """Return formatted choices for user display."""
        pass