"""
Game flow management for handling different game modes.

This module centralizes the logic for managing game flow, including
standard rounds and best-of-X series.
"""

from typing import List
from src.game_utils.game_rules import GameRules
from src.constants import GameConstants, GameMessages
from game_engine import GameEngine


class GameFlowManager:
    """
    Manages the flow of game execution.

    This class handles different game modes (standard rounds, best-of-X)
    and delegates execution to the GameEngine.
    """

    def __init__(self, rules: GameRules, output_provider):
        self.rules = rules
        self.output_provider = output_provider
        self.game_engine = GameEngine(rules, output_provider)

    def play_standard_rounds(self, rounds_to_play: int, player_1, 
                             player_2, score_manager) -> None:
        """
        Play a specified number of rounds.

        Args:
            rounds_to_play: Number of rounds to play
            player_1: The first player
            player_2: The second player
            score_manager: The score manager to track scores
        """
        self.game_engine.play_standard_rounds(rounds_to_play, player_1, player_2, score_manager)

    def play_best_of_series(self, player_1, player_2,
                            score_manager, max_rounds: int = None,
                            win_threshold: int = None) -> None:
        """
        Play a best-of-X series.

        Args:
            player_1: The first player
            player_2: The second player
            score_manager: The score manager to track scores
            max_rounds: Maximum number of rounds in series
            win_threshold: Points needed to win series
        """
        self.game_engine.play_best_of_series(player_1, player_2, score_manager, 
                                             max_rounds, win_threshold)
