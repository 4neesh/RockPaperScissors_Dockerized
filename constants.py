"""
Constants and configuration values for the Rock Paper Scissors game.

This module centralizes all magic numbers, hardcoded strings, and configuration values
used throughout the game to improve maintainability and reduce coupling.
"""

from enum import Enum


class GameConfig:
    """Game-wide configuration constants."""

    # Core game settings
    EXIT_COMMAND = "e"
    MAX_ROUNDS = 99
    GAME_TYPE = "rps"
    DEFAULT_SCORE_MANAGER_TYPE = "standard"
    MOVE_TIME_LIMIT = 10  # seconds
    DEFAULT_TIME_LIMIT = 10  # seconds

    # Game modes
    BEST_OF_5_ROUNDS = 5
    BEST_OF_5_WINNING_SCORE = 3
    REQUIRED_PLAYERS = 2

    # Player settings
    MAX_NAME_LENGTH = 20
    PLAYER_ID_OFFSET = 1


class HandGestureConfig:
    """Hand gesture related constants."""

    ROCK_VALUE = 1
    PAPER_VALUE = 2
    SCISSORS_VALUE = 3


class ScoringConfig:
    """Scoring system constants."""

    # Standard scoring
    WIN_POINTS = 1
    DRAW_POINTS = 0.5
    LOSS_POINTS = 0

    # Result indicators
    PLAYER_1_WIN = 1
    PLAYER_2_WIN = -1
    DRAW_RESULT = 0

    # Streak scoring
    FIRST_WIN_POINTS = 1
    SECOND_WIN_POINTS = 2
    THIRD_PLUS_WIN_POINTS = 3


class UIConfig:
    """User interface and display constants."""

    # Table formatting
    PLAYER_COLUMN_WIDTH = 20
    SCORE_COLUMN_WIDTH = 10
    TABLE_SEPARATOR_WIDTH = 30
    MOVE_SEPARATOR_LENGTH = 50

    # Game mode display
    GAME_MODE_START_INDEX = 1


class Messages:
    """Centralized message strings for consistent UI."""

    # Game introduction
    GAME_NAME = "Paper Scissors Rock"
    GAME_INTRO_FORMAT = "We're playing {game_name}!"

    # Round messages
    ROUND_FORMAT = "\nRound {round_number} of {total_rounds}"
    MOVES_FORMAT = "\n{player1_name} ({player1_move})  |  {player2_name} ({player2_move})"
    MOVES_SEPARATOR = "-" * UIConfig.MOVE_SEPARATOR_LENGTH

    # Timeout messages
    TIMEOUT_MESSAGE = "\nTime's up!"
    BOTH_TIMEOUT_FORMAT = "\nBoth players took too long to respond. Round is a draw!"
    PLAYER_TIMEOUT_FORMAT = "\n{timeout_player} took too long to respond. {winner_player} wins this round!"

    # Best of 5 messages
    BEST_OF_5_OPTION = "bo5"
    BEST_OF_5_WIN_FORMAT = "\n{winner} wins the Best of 5 series!"
    BEST_OF_5_DRAW = "Best of 5 series finishes in a draw!"

    # Score display
    PLAYER_HEADER = "Player"
    SCORE_HEADER = "Score"
    TABLE_SEPARATOR = "-" * UIConfig.TABLE_SEPARATOR_WIDTH
    SCORE_ROW_FORMAT = "{name:<{name_width}}{score:<{score_width}}"

    # Game result messages
    GAME_WIN_FORMAT = "\n{winner} won with a score of {winner_score} to {loser_score}"
    GAME_DRAW = "\nThe game is a draw!"
    GAME_ENDING = "Game is ending"

    # Draw descriptions
    DRAW_DESCRIPTION_FORMAT = "{move1} vs {move2} is a draw"

    # Input prompts
    GAME_MODE_PROMPT = "Please enter a number to select a game mode: {modes} \n"
    PLAYER_NAME_PROMPT = "Please enter player {player_id} name: "
    PLAY_AGAIN_PROMPT = "\nEnter 'y' to replay, or any key to exit \n"
    ROUNDS_PROMPT = "Enter number of rounds to play (1-{max_rounds}) or '{best_of_5}' for Best of 5 mode: "
    MOVE_PROMPT = "Player {player_id}: Enter your move ({choices}), or enter '{exit_cmd}' to exit the game"
    MOVE_PROMPT_WITH_TIME = "Player {player_id}: Enter your move ({choices}), or enter '{exit_cmd}' to exit the game - You have {time_limit} seconds to respond"
    ROUNDS_REQUEST_PROMPT = "How many rounds of Rock, Paper, Scissors would you like to play? (Max: {max_rounds}) \n"

    # Error messages
    GAME_MODE_ERROR = "Invalid selection. Please enter a number that corresponds to a game mode."
    NAME_ERROR = "Invalid input. Name cannot be empty and must be shorter than {max_length} characters."
    ROUNDS_ERROR = "Invalid input. Please enter a valid number between 1 and {max_rounds}."
    GESTURE_ERROR = "Invalid input. Please enter a valid Hand Gesture number."

    # Computer player naming
    COMPUTER_PLAYER_NAME_FORMAT = "Computer {player_id}"

    # Gesture choice formatting
    GESTURE_CHOICE_FORMAT = "{value} = {name}"

    # Game mode formatting
    GAME_MODE_FORMAT = "\n{index} = {mode_name}"

    # Streak display formatting
    STREAK_DISPLAY_FORMAT = "{player_name} (streak: {streak})"

    # Interaction descriptions
    ROCK_BLUNTS_SCISSORS = "blunts"
    PAPER_WRAPS_ROCK = "wraps"
    SCISSORS_CUTS_PAPER = "cuts"
    INTERACTION_FORMAT = "{winner_move} {action} {loser_move}"
    NO_DESCRIPTION_FORMAT = "No description available for {move1} vs {move2}"

    # Replay prompt responses
    REPLAY_YES = "y"


class Timeouts:
    """Timeout and timing related constants."""

    DEFAULT_ALARM_SIGNAL = 0  # Value to cancel alarm


class ValidationConfig:
    """Input validation constants."""

    MIN_ROUNDS = 1
    MIN_PLAYER_ID = 1
    EMPTY_STRING_LENGTH = 0


class FactoryConfig:
    """Factory pattern related constants."""

    UNSUPPORTED_GAME_ERROR = "Unsupported game type: {game_type}"


class ErrorMessages:
    """Error message templates."""

    INVALID_GAME_MODE_ERROR = "Invalid Game Mode created, all modes must be set-up for exactly {required_players} players"