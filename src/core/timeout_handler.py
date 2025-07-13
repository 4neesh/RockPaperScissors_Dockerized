"""
Centralized timeout handling for game rounds.

This module provides a clean way to handle player timeouts in a consistent
manner across all game types.
"""

from typing import Optional, Tuple
from enum import Enum

from src.core.game_move import GameMove
from src.players.player import Player
from game_engine import GameEngine
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
                       game_engine: GameEngine) -> Tuple[TimeoutResult, Optional[int]]:
        """
        Handle timeout scenarios for a round.

        Args:
            player_1: The first player
            player_2: The second player
            move_1: The first player's move (None if timed out)
            move_2: The second player's move (None if timed out)
            game_engine: the game engine to update scores

        Returns:
            Tuple of (TimeoutResult, score_update)
            score_update is None if no timeout occurred
        """
        if move_1 is None and move_2 is None:
            return self._handle_both_timeout(game_engine)
        elif move_1 is None:
            return self._handle_player_1_timeout(player_1, player_2, game_engine)
        elif move_2 is None:
            return self._handle_player_2_timeout(player_1, player_2, game_engine)
        else:
            return TimeoutResult.BOTH_VALID, None

    def _handle_both_timeout(self, game_engine: GameEngine) -> Tuple[TimeoutResult, int]:
        """Handle case where both players timed out."""
        print(GameMessages.BOTH_TIMEOUT)
        # Create dummy moves to simulate a draw
        valid_moves = game_engine.rules.get_valid_moves()
        if valid_moves:
            dummy_move = valid_moves[0]
            game_engine.process_round(dummy_move, dummy_move)  # Guaranteed draw
        self.output_provider.output_scores_table(game_engine.get_scores())
        return TimeoutResult.BOTH_TIMEOUT, ScoringConstants.DRAW

    def _handle_player_1_timeout(self, player_1: Player, player_2: Player,
                                game_engine: GameEngine) -> Tuple[TimeoutResult, int]:
        """Handle case where player 1 timed out."""
        print(GameMessages.PLAYER_TIMEOUT.format(
            loser=player_1.get_name(),
            winner=player_2.get_name()
        ))
        # Simulate round with timeout - auto win for player 2
        valid_moves = game_engine.rules.get_valid_moves()
        if valid_moves:
            # Use valid moves to give player 2 the win
            p2_move = player_2.make_move() or valid_moves[0]
            # Find a move that would lose to p2's move
            for potential_move in valid_moves:
                result = game_engine.determine_result(potential_move, p2_move)
                if result == ScoringConstants.PLAYER_2_WIN:
                    game_engine.process_round(potential_move, p2_move)
                    break
            else:
                # If no losing move found, just process with the same move (draw)
                # and manually update score
                game_engine.process_round(p2_move, p2_move)
                game_engine._scores[player_2.get_name()] += ScoringConstants.STANDARD_WIN_POINTS
                
        self.output_provider.output_scores_table(game_engine.get_scores())
        return TimeoutResult.PLAYER_1_TIMEOUT, ScoringConstants.PLAYER_2_WIN

    def _handle_player_2_timeout(self, player_1: Player, player_2: Player,
                                game_engine: GameEngine) -> Tuple[TimeoutResult, int]:
        """Handle case where player 2 timed out."""
        print(GameMessages.PLAYER_TIMEOUT.format(
            loser=player_2.get_name(),
            winner=player_1.get_name()
        ))
        # Simulate round with timeout - auto win for player 1
        valid_moves = game_engine.rules.get_valid_moves()
        if valid_moves:
            # Use valid moves to give player 1 the win
            p1_move = player_1.make_move() or valid_moves[0]
            # Find a move that would lose to p1's move
            for potential_move in valid_moves:
                result = game_engine.determine_result(p1_move, potential_move)
                if result == ScoringConstants.PLAYER_1_WIN:
                    game_engine.process_round(p1_move, potential_move)
                    break
            else:
                # If no losing move found, just process with the same move (draw)
                # and manually update score
                game_engine.process_round(p1_move, p1_move)
                game_engine._scores[player_1.get_name()] += ScoringConstants.STANDARD_WIN_POINTS
                
        self.output_provider.output_scores_table(game_engine.get_scores())
        return TimeoutResult.PLAYER_2_TIMEOUT, ScoringConstants.PLAYER_1_WIN
