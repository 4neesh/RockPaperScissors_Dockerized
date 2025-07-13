"""
Game Engine for Rock-Paper-Scissors game.

This module provides a GameEngine class that encapsulates the core game logic
including move validation, result determination, and score management.
"""

from typing import List, Optional, Tuple, Dict, Any

from src.core.game_move import GameMove
from src.game_utils.game_rules import GameRules
from src.game_utils.score_manager import ScoreManager
from src.players.player import Player
from src.constants import GameConstants, ScoringConstants, GameMessages


class GameEngine:
    """
    GameEngine encapsulates the core game logic of the Rock-Paper-Scissors game.
    
    This class is responsible for:
    - Move validation
    - Winner determination
    - Score tracking
    - Game flow management
    """
    
    def __init__(self, rules: GameRules, output_provider):
        """
        Initialize the GameEngine with game rules and an output provider.
        
        Args:
            rules: Rules for the specific game type
            output_provider: Provider for game output
        """
        self.rules = rules
        self.output_provider = output_provider
        
    def validate_game_option(self, option: str, max_rounds: int) -> bool:
        """
        Validate the game option input.
        
        Args:
            option: The user's input
            max_rounds: Maximum number of rounds allowed
        
        Returns:
            True if valid, False otherwise
        """
        # Check for best of 5 option
        if option == GameConstants.BEST_OF_5_COMMAND:
            return True
            
        # Check for valid rounds number
        if option.isdigit():
            rounds = int(option)
            if GameConstants.MIN_ROUNDS <= rounds <= max_rounds:
                return True
                
        # Invalid input
        self.output_provider.output_rounds_error(max_rounds)
        return False
        
    def play_standard_rounds(self, rounds_to_play: int, player_1: Player,
                          player_2: Player, score_manager: ScoreManager) -> None:
        """
        Play a specified number of rounds.
        
        Args:
            rounds_to_play: Number of rounds to play
            player_1: The first player
            player_2: The second player
            score_manager: The score manager to track scores
        """
        for round_number in range(1, rounds_to_play + 1):
            self._execute_round(player_1, player_2, score_manager, round_number, rounds_to_play)
            
    def play_best_of_series(self, player_1: Player, player_2: Player,
                         score_manager: ScoreManager, max_rounds: int = None,
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
        if max_rounds is None:
            max_rounds = GameConstants.BEST_OF_SERIES_ROUNDS
        if win_threshold is None:
            win_threshold = GameConstants.BEST_OF_SERIES_WIN_THRESHOLD
            
        round_number = 1
        
        while (round_number <= max_rounds and
               score_manager.get_player_score(player_1.get_name()) < win_threshold and
               score_manager.get_player_score(player_2.get_name()) < win_threshold):
            self._execute_round(player_1, player_2, score_manager, round_number, max_rounds)
            round_number += 1
            
        # Provide feedback about series result
        self._announce_series_result(player_1, player_2, score_manager)
        
    def _execute_round(self, player_1: Player, player_2: Player,
                     score_manager: ScoreManager, round_number: int = None,
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
        # Display round header if numbers provided
        if round_number is not None and total_rounds is not None:
            self.output_provider.output_round_number(round_number, total_rounds)
            
        # Get moves from both players
        move_1 = player_1.make_move()
        move_2 = player_2.make_move()
        
        # Handle timeout cases
        timeout_result, score_update = self._handle_timeout(
            player_1, player_2, move_1, move_2, score_manager
        )
        
        if timeout_result != "both_valid":
            return False  # Timeout occurred
            
        # Normal case - both players made valid moves
        self._process_valid_moves(player_1, player_2, move_1, move_2, score_manager)
        return True
        
    def _handle_timeout(self, player_1: Player, player_2: Player,
                      move_1: Optional[GameMove], move_2: Optional[GameMove],
                      score_manager: ScoreManager) -> Tuple[str, Optional[int]]:
        """
        Handle timeout scenarios for a round.
        
        Args:
            player_1: The first player
            player_2: The second player
            move_1: The first player's move (None if timed out)
            move_2: The second player's move (None if timed out)
            score_manager: The score manager to update
            
        Returns:
            Tuple of (timeout_result, score_update)
            score_update is None if no timeout occurred
        """
        if move_1 is None and move_2 is None:
            return self._handle_both_timeout(score_manager)
        elif move_1 is None:
            return self._handle_player_1_timeout(player_1, player_2, score_manager)
        elif move_2 is None:
            return self._handle_player_2_timeout(player_1, player_2, score_manager)
        else:
            return "both_valid", None
            
    def _handle_both_timeout(self, score_manager: ScoreManager) -> Tuple[str, int]:
        """Handle case where both players timed out."""
        print(GameMessages.BOTH_TIMEOUT)
        score_manager.update_scores_for_round(ScoringConstants.DRAW)
        score_manager.return_leaderboard()
        return "both_timeout", ScoringConstants.DRAW
        
    def _handle_player_1_timeout(self, player_1: Player, player_2: Player,
                               score_manager: ScoreManager) -> Tuple[str, int]:
        """Handle case where player 1 timed out."""
        print(GameMessages.PLAYER_TIMEOUT.format(
            loser=player_1.get_name(),
            winner=player_2.get_name()
        ))
        score_manager.update_scores_for_round(ScoringConstants.PLAYER_2_WIN)
        score_manager.return_leaderboard()
        return "player_1_timeout", ScoringConstants.PLAYER_2_WIN
        
    def _handle_player_2_timeout(self, player_1: Player, player_2: Player,
                               score_manager: ScoreManager) -> Tuple[str, int]:
        """Handle case where player 2 timed out."""
        print(GameMessages.PLAYER_TIMEOUT.format(
            loser=player_2.get_name(),
            winner=player_1.get_name()
        ))
        score_manager.update_scores_for_round(ScoringConstants.PLAYER_1_WIN)
        score_manager.return_leaderboard()
        return "player_2_timeout", ScoringConstants.PLAYER_1_WIN
        
    def _process_valid_moves(self, player_1: Player, player_2: Player,
                           move_1: GameMove, move_2: GameMove, score_manager: ScoreManager):
        """Process a round where both players made valid moves."""
        # Display the moves
        self.output_provider.output_round_moves(player_1, player_2, move_1, move_2)
        
        # Get interaction description
        interaction_description = self.rules.get_interaction_description(move_1, move_2)
        self.output_provider.output_round_description(interaction_description)
        
        # Determine result and update scores
        round_result = self.rules.determine_result(move_1, move_2)
        score_manager.update_scores_for_round(round_result)
        score_manager.return_leaderboard()
        
    def _announce_series_result(self, player_1: Player, player_2: Player,
                              score_manager: ScoreManager) -> None:
        """Announce the result of a best-of series."""
        p1_score = score_manager.get_player_score(player_1.get_name())
        p2_score = score_manager.get_player_score(player_2.get_name())
        
        if p1_score > p2_score:
            print(GameMessages.BEST_OF_5_WINNER.format(winner=player_1.get_name()))
        elif p2_score > p1_score:
            print(GameMessages.BEST_OF_5_WINNER.format(winner=player_2.get_name()))
        else:
            print(GameMessages.BEST_OF_5_DRAW)
