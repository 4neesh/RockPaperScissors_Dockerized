"""
Constants specific to Rock-Paper-Scissors game.

This module contains all RPS-specific constants, separated from
the generic game constants to improve modularity.
"""

from typing import Final


class RPSConstants:
    """Constants specific to Rock-Paper-Scissors gameplay."""

    # Game identification
    GAME_NAME: Final[str] = "Paper Scissors Rock"
    GAME_TYPE: Final[str] = "rps"

    # Move values
    ROCK_VALUE: Final[int] = 1
    PAPER_VALUE: Final[int] = 2
    SCISSORS_VALUE: Final[int] = 3

    # Move names
    ROCK_NAME: Final[str] = "Rock"
    PAPER_NAME: Final[str] = "Paper"
    SCISSORS_NAME: Final[str] = "Scissors"

    # Interaction descriptions (what each move does to others)
    ROCK_ACTION: Final[str] = "blunts"
    PAPER_ACTION: Final[str] = "wraps"
    SCISSORS_ACTION: Final[str] = "cuts"

    # Display formatting
    MOVE_FORMAT: Final[str] = "{value} = {name}"


class RPSGameConfig:
    """Configuration for Rock-Paper-Scissors game."""

    # Default game settings
    DEFAULT_MAX_ROUNDS: Final[int] = 99
    DEFAULT_TIME_LIMIT: Final[int] = 10

    # Scoring system
    SCORE_MANAGER_TYPE: Final[str] = "standard"

    # Game prompts
    ROUNDS_PROMPT: Final[str] = "How many rounds of Rock, Paper, Scissors would you like to play? (Max: {max}) \n"