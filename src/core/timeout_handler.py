"""
Centralized timeout handling for game rounds.

This module now delegates to the GameEngine for timeout handling.
"""

from typing import Optional, Tuple
from enum import Enum

from src.core.game_move import GameMove
from src.players.player import Player
from game_engine import GameEngine
from src.game_utils.game_rules import GameRules


class TimeoutResult(Enum):
    """Represents the result of a timeout check."""
    BOTH_VALID = "both_valid"
    BOTH_TIMEOUT = "both_timeout"
    PLAYER_1_TIMEOUT = "player_1_timeout"
    PLAYER_2_TIMEOUT = "player_2_timeout"


class TimeoutHandler:
    """
    Handles timeout logic for game rounds by delegating to the GameEngine.
    """

    def __init__(self, output_provider):
        self.output_provider = output_provider
        # Since we need rules for the GameEngine, we'll have the rules passed in handle_timeout
        self.game_engine = None

    def handle_timeout(self, player_1: Player, player_2: Player,
                       move_1: Optional[GameMove], move_2: Optional[GameMove],
                       score_manager, rules: GameRules = None) -> Tuple[TimeoutResult, Optional[int]]:
        """
        Handle timeout scenarios for a round.

        Args:
            player_1: The first player
            player_2: The second player
            move_1: The first player's move (None if timed out)
            move_2: The second player's move (None if timed out)
            score_manager: The score manager to update
            rules: Game rules (required for first call to initialize GameEngine)

        Returns:
            Tuple of (TimeoutResult, score_update)
            score_update is None if no timeout occurred
        """
        # Initialize game engine if not already done
        if self.game_engine is None and rules is not None:
            self.game_engine = GameEngine(rules, self.output_provider)
        
        result, score_update = self.game_engine._handle_timeout(
            player_1, player_2, move_1, move_2, score_manager
        )
        
        # Map string result to TimeoutResult enum
        timeout_result_map = {
            "both_valid": TimeoutResult.BOTH_VALID,
            "both_timeout": TimeoutResult.BOTH_TIMEOUT,
            "player_1_timeout": TimeoutResult.PLAYER_1_TIMEOUT,
            "player_2_timeout": TimeoutResult.PLAYER_2_TIMEOUT,
        }
        
        return timeout_result_map.get(result, TimeoutResult.BOTH_VALID), score_update
