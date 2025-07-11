"""
Central configuration and constants module for the game system.

This module contains generic game constants that apply to all game types.
Game-specific constants are kept in their respective modules.
"""

from typing import Final


class GameConstants:
    """Generic constants for the game system."""

    # Game flow configuration
    MAX_ROUNDS: Final[int] = 99
    MIN_ROUNDS: Final[int] = 1
    BEST_OF_SERIES_ROUNDS: Final[int] = 5
    BEST_OF_SERIES_WIN_THRESHOLD: Final[int] = 3
    REQUIRED_PLAYER_COUNT: Final[int] = 2

    # Time limits
    DEFAULT_MOVE_TIME_LIMIT: Final[int] = 10  # seconds

    # Score manager types
    SCORE_MANAGER_STANDARD: Final[str] = "standard"
    SCORE_MANAGER_STREAK: Final[str] = "streak"

    # Game mode options
    BEST_OF_5_COMMAND: Final[str] = "bo5"

    # Exit command
    EXIT_COMMAND: Final[str] = "e"


class PlayerConstants:
    """Constants related to player configuration."""

    # Name constraints
    MAX_NAME_LENGTH: Final[int] = 20
    MIN_NAME_LENGTH: Final[int] = 1

    # Default time limit for moves
    DEFAULT_TIME_LIMIT: Final[int] = 10  # seconds

    # Computer player name prefix
    COMPUTER_NAME_PREFIX: Final[str] = "Computer"


class ScoringConstants:
    """Constants related to scoring systems."""

    # Standard scoring
    STANDARD_WIN_POINTS: Final[float] = 1.0
    STANDARD_DRAW_POINTS: Final[float] = 0.5
    STANDARD_LOSS_POINTS: Final[float] = 0.0

    # Streak scoring
    STREAK_FIRST_WIN_POINTS: Final[int] = 1
    STREAK_SECOND_WIN_POINTS: Final[int] = 2
    STREAK_THIRD_PLUS_WIN_POINTS: Final[int] = 3
    STREAK_DRAW_POINTS: Final[int] = 0

    # Result codes
    PLAYER_1_WIN: Final[int] = 1
    PLAYER_2_WIN: Final[int] = -1
    DRAW: Final[int] = 0


class DisplayConstants:
    """Constants related to display formatting."""

    # Table formatting
    SCORE_TABLE_NAME_WIDTH: Final[int] = 20
    SCORE_TABLE_SCORE_WIDTH: Final[int] = 10
    SCORE_TABLE_SEPARATOR_LENGTH: Final[int] = 30
    ROUND_SEPARATOR_LENGTH: Final[int] = 50

    # Column headers
    PLAYER_COLUMN_HEADER: Final[str] = "Player"
    SCORE_COLUMN_HEADER: Final[str] = "Score"

    # Separator characters
    TABLE_SEPARATOR_CHAR: Final[str] = "-"

    # Formatting strings
    STREAK_FORMAT: Final[str] = "{name} (streak: {streak})"


class GameMessages:
    """String constants for game messages and prompts."""

    # Game introduction
    GAME_INTRO: Final[str] = "We're playing {game}!"
    GAME_ENDING: Final[str] = "Game is ending"

    # Game mode selection
    GAME_MODE_PROMPT: Final[str] = "Please enter a number to select a game mode: {modes} \n"
    GAME_MODE_ERROR: Final[str] = "Invalid selection. Please enter a number that corresponds to a game mode."
    GAME_MODE_FORMAT: Final[str] = "\n{index} = {mode_name}"

    # Player setup
    PLAYER_NAME_PROMPT: Final[str] = "Please enter player {player_id} name: "
    PLAYER_NAME_ERROR: Final[str] = "Invalid input. Name cannot be empty and must be shorter than {max_length} characters."

    # Round setup
    ROUNDS_PROMPT: Final[str] = "Enter number of rounds to play ({min}-{max}) or '{bo5}' for Best of 5 mode: "
    ROUNDS_ERROR: Final[str] = "Invalid input. Please enter a valid number between {min} and {max}."

    # Gameplay
    MOVE_PROMPT: Final[str] = "Player {player_id}: Enter your move ({choices}), or enter '{exit}' to exit the game"
    MOVE_TIME_WARNING: Final[str] = " - You have {time_limit} seconds to respond"
    TIMEOUT_MESSAGE: Final[str] = "\nTime's up!"
    BOTH_TIMEOUT: Final[str] = "\nBoth players took too long to respond. Round is a draw!"
    PLAYER_TIMEOUT: Final[str] = "\n{loser} took too long to respond. {winner} wins this round!"
    INVALID_GESTURE: Final[str] = "Invalid input. Please enter a valid move number."

    # Round display
    ROUND_HEADER: Final[str] = "\nRound {current} of {total}"
    ROUND_MOVES: Final[str] = "\n{player1} ({move1})  |  {player2} ({move2})"

    # Results
    DRAW_ROUND: Final[str] = "\n{move1} vs {move2} is a draw."
    DRAW_GAME: Final[str] = "\nThe game is a draw!"
    GAME_WINNER: Final[str] = "\n{winner} won with a score of {winner_score} to {loser_score}"
    BEST_OF_5_WINNER: Final[str] = "\n{winner} wins the Best of 5 series!"
    BEST_OF_5_DRAW: Final[str] = "Best of 5 series finishes in a draw!"

    # Replay
    REPLAY_PROMPT: Final[str] = "\nEnter 'y' to replay, or any key to exit \n"
    REPLAY_YES: Final[str] = "y"

    # Move interactions
    DRAW_DESCRIPTION: Final[str] = "{move1} vs {move2} is a draw"
    WIN_DESCRIPTION: Final[str] = "{winner} {action} {loser}"
    NO_DESCRIPTION: Final[str] = "No description available for {move1} vs {move2}"

    # Error messages
    UNSUPPORTED_GAME_TYPE: Final[str] = "Unsupported game type: {game_type}"
    UNSUPPORTED_SCORE_TYPE: Final[str] = "Unsupported score manager type: {manager_type}"
    INVALID_GAME_MODE: Final[str] = "Invalid Game Mode created, all modes must be set-up for exactly {count} players"
    NO_RULE_DEFINED: Final[str] = "No rule defined between {move1} and {move2}"