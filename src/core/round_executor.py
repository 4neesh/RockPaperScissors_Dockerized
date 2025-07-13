"""
Round execution logic for games.

This module handles the execution of individual rounds, including move
collection, timeout handling, and result determination.
"""

from typing import Optional, Tuple

from src.core.game_move import GameMove
from src.core.timeout_handler import TimeoutHandler, TimeoutResult
from src.players.player import Player
from game_engine import GameEngine
from src.constants import ScoringConstants


class RoundExecutor:
    """
    Handles the execution of individual game rounds.

    This class encapsulates all the logic for executing a single round,
    including move collection, timeout handling, and result determination.
    """

    def __init__(self, game_engine: GameEngine, output_provider):
        self.game_engine = game_engine
        self.output_provider = output_provider
        self.timeout_handler = TimeoutHandler(output_provider)

    def execute_round(self, player_1: Player, player_2: Player,
                      round_number: int = None,
                      total_rounds: int = None) -> bool:
        """
        Execute a single round of the game.

        Args:
            player_1: The first player
            player_2: The second player
            round_number: Current round number (for display)
            total_rounds: Total number of rounds (for display)

        Returns:
            True if round completed normally, False if timeout occurred
        """
        # Display round header if numbers provided
        if round_number is not None and total_rounds is not None:
            self.output_provider.output_round_number(round_number, total_rounds)

        # Get moves from both players
        move_1 = player_1.make_move()
        move_2 = player_2.make_move()

        # Handle timeout cases
        timeout_result, score_update = self.timeout_handler.handle_timeout(
            player_1, player_2, move_1, move_2, self.game_engine
        )

        if timeout_result != TimeoutResult.BOTH_VALID:
            return False  # Timeout occurred

        # Normal case - both players made valid moves
        self._process_valid_moves(player_1, player_2, move_1, move_2)
        return True

    def _process_valid_moves(self, player_1: Player, player_2: Player,
                             move_1: GameMove, move_2: GameMove):
        """Process a round where both players made valid moves."""
        # Display the moves
        self.output_provider.output_round_moves(player_1, player_2, move_1, move_2)

        # Process round with game engine
        round_result, interaction_description = self.game_engine.process_round(move_1, move_2)
        
        # Display interaction description
        self.output_provider.output_round_description(interaction_description)

        # Display updated scores
        scores = self.game_engine.get_scores()
        self.output_provider.output_scores_table(scores)
