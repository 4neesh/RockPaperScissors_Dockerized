"""
Rock-Paper-Scissors move implementation.

This module implements the GameMove interface for RPS-specific moves,
making it easy to extend the game framework to other game types.
"""

import random
from enum import Enum
from typing import List, Any

from src.games.rps.rps_constants import RPSConstants


class RPSMove(Enum):
    ROCK = (1, "Rock")
    PAPER = (2, "Paper")
    SCISSORS = (3, "Scissors")

    def __init__(self, move_value: int, display_name: str):
        self._move_value = move_value
        self._display_name = display_name

    def get_value(self) -> int:
        return self._move_value

    def get_name(self) -> str:
        return self._display_name

    def __str__(self) -> str:
        return self._display_name

    def __eq__(self, other) -> bool:
        if isinstance(other, RPSMove):
            return self._move_value == other._move_value
        return False

    def __hash__(self) -> int:
        return hash(self._move_value)

    @classmethod
    def get_all_moves(cls) -> List['RPSMove']:
        return list(cls)

    @classmethod
    def get_random_move(cls) -> 'RPSMove':
        return random.choice(list(cls))

    @classmethod
    def get_move_by_value(cls, value: int) -> 'RPSMove':
        for move in cls:
            if move.get_value() == value:
                return move
        raise ValueError(f"No RPS move with value {value}")

    @classmethod
    def validate_value(cls, value: Any) -> bool:
        return isinstance(value, int) and any(move.get_value() == value for move in cls)

    @classmethod
    def get_formatted_choices(cls) -> List[str]:
        return [RPSConstants.MOVE_FORMAT.format(
            value=move.get_value(),
            name=move.get_name()
        ) for move in cls]
