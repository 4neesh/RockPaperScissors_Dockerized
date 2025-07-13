"""
Round execution logic for games.

This module is now just a wrapper for GameEngine's round execution logic.
"""

from src.game_utils.game_rules import GameRules
from game_engine import GameEngine


class RoundExecutor:
    """
    Handles the execution of individual game rounds.

    This class now delegates to the GameEngine for round execution.
    """

    def __init__(self, rules: GameRules, output_provider):
        self.rules = rules
        self.output_provider = output_provider
        self.game_engine = GameEngine(rules, output_provider)

    def execute_round(self, player_1, player_2,
                      score_manager, round_number: int = None,
                      total_rounds: int = None) -> bool:
        """
        Execute a single round of the game.

        Args:
            player_1: The first player
            player_2: The second player
            score_manager: The score manager to update
            round_number: Current round number (for display)
            total_rounds: Total number of rounds (for display)

        Returns:
            True if round completed normally, False if timeout occurred
        """
        return self.game_engine._execute_round(player_1, player_2, score_manager, 
                                              round_number, total_rounds)
