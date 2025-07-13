"""
Game flow management for handling different game modes.

This module centralizes the logic for managing game flow, including
standard rounds and best-of-X series.
"""

from typing import List
from src.core.round_executor import RoundExecutor
from src.players.player import Player
from game_engine import GameEngine
from src.constants import GameConstants, GameMessages


class GameFlowManager:
    """
    Manages the flow of game execution.

    This class handles different game modes (standard rounds, best-of-X)
    and delegates individual round execution to the RoundExecutor.
    """

    def __init__(self, game_engine: GameEngine, output_provider):
        self.game_engine = game_engine
        self.output_provider = output_provider
        self.round_executor = RoundExecutor(game_engine, output_provider)

    def play_standard_rounds(self, rounds_to_play: int, player_1: Player,
                             player_2: Player) -> None:
        """
        Play a specified number of rounds.

        Args:
            rounds_to_play: Number of rounds to play
            player_1: The first player
            player_2: The second player
        """
        for round_number in range(1, rounds_to_play + 1):
            self.round_executor.execute_round(
                player_1, player_2, round_number, rounds_to_play
            )

    def play_best_of_series(self, player_1: Player, player_2: Player,
                            max_rounds: int = None,
                            win_threshold: int = None) -> None:
        """
        Play a best-of-X series.

        Args:
            player_1: The first player
            player_2: The second player
            max_rounds: Maximum number of rounds in series
            win_threshold: Points needed to win series
        """
        if max_rounds is None:
            max_rounds = GameConstants.BEST_OF_SERIES_ROUNDS
        if win_threshold is None:
            win_threshold = GameConstants.BEST_OF_SERIES_WIN_THRESHOLD

        round_number = 1

        while (round_number <= max_rounds and
               not self.game_engine.is_series_over(win_threshold)):
            self.round_executor.execute_round(
                player_1, player_2, round_number, max_rounds
            )
            round_number += 1

        # Provide feedback about series result
        self._announce_series_result()

    def _announce_series_result(self) -> None:
        """Announce the result of a best-of series."""
        winner_name, winner_score, loser_score = self.game_engine.determine_winner()
        
        if winner_name:
            print(GameMessages.BEST_OF_5_WINNER.format(winner=winner_name))
        else:
            print(GameMessages.BEST_OF_5_DRAW)
