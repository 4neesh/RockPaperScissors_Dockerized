"""
Centralized timeout handling for game rounds.

This module provides a clean way to handle player timeouts in a consistent
manner across all game types.
"""

from typing import Optional, Tuple
from enum import Enum

from src.core.game_move import GameMove
from src.players.player import Player
from src.constants import GameMessages, ScoringConstants


class TimeoutResult(Enum):
    """Represents the result of a timeout check."""
    BOTH_VALID = "both_valid"
    BOTH_TIMEOUT = "both_timeout"
    PLAYER_1_TIMEOUT = "player_1_timeout"
    PLAYER_2_TIMEOUT = "player_2_timeout"


class TimeoutHandler:
    """
    Handles timeout logic for game rounds.

    This class centralizes all timeout handling logic that was previously
    duplicated across different game methods.
    """

    def __init__(self, output_provider):
        self.output_provider = output_provider

    def handle_timeout(self, player_1: Player, player_2: Player,
                       move_1: Optional[GameMove], move_2: Optional[GameMove],
                       score_manager) -> Tuple[TimeoutResult, Optional[int]]:
        """
        Handle timeout scenarios for a round.

        Args:
            player_1: The first player
            player_2: The second player
            move_1: The first player's move (None if timed out)
            move_2: The second player's move (None if timed out)
            score_manager: The score manager to update

        Returns:
            Tuple of (TimeoutResult, score_update)
            score_update is None if no timeout occurred
        """
        if move_1 is None and move_2 is None:
            return self._handle_both_timeout(score_manager)
        elif move_1 is None:
            return self._handle_player_1_timeout(player_1, player_2, score_manager)
        elif move_2 is None:
            return self._handle_player_2_timeout(player_1, player_2, score_manager)
        else:
            return TimeoutResult.BOTH_VALID, None

    def _handle_both_timeout(self, score_manager) -> Tuple[TimeoutResult, int]:
        """Handle case where both players timed out."""
        print(GameMessages.BOTH_TIMEOUT)
        score_manager.update_scores_for_round(ScoringConstants.DRAW)
        score_manager.return_leaderboard()
        return TimeoutResult.BOTH_TIMEOUT, ScoringConstants.DRAW

    def _handle_player_1_timeout(self, player_1: Player, player_2: Player,
                                 score_manager) -> Tuple[TimeoutResult, int]:
        """Handle case where player 1 timed out."""
        print(GameMessages.PLAYER_TIMEOUT.format(
            loser=player_1.get_name(),
            winner=player_2.get_name()
        ))
        score_manager.update_scores_for_round(ScoringConstants.PLAYER_2_WIN)
        score_manager.return_leaderboard()
        return TimeoutResult.PLAYER_1_TIMEOUT, ScoringConstants.PLAYER_2_WIN

    def _handle_player_2_timeout(self, player_1: Player, player_2: Player,
                                 score_manager) -> Tuple[TimeoutResult, int]:
        """Handle case where player 2 timed out."""
        print(GameMessages.PLAYER_TIMEOUT.format(
            loser=player_2.get_name(),
            winner=player_1.get_name()
        ))
        score_manager.update_scores_for_round(ScoringConstants.PLAYER_1_WIN)
        score_manager.return_leaderboard()
        return TimeoutResult.PLAYER_2_TIMEOUT, ScoringConstants.PLAYER_1_WIN