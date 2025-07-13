"""
Game engine that encapsulates core game logic.

This module provides a GameEngine class that handles move validation, winner determination,
and score tracking, independent of the user interface or game flow.
"""

from typing import Tuple, Optional, List
from src.core.game_move import GameMove
from src.game_utils.game_rules import GameRules
from src.constants import ScoringConstants, GameMessages
from src.players.player import Player


class GameEngine:
    """
    GameEngine encapsulates the core game logic.
    
    This class is responsible for:
    - Validating moves
    - Determining winners
    - Tracking and updating scores
    - Providing game state information
    """
    
    def __init__(self, rules: GameRules):
        """
        Initialize the game engine with the appropriate game rules.
        
        Args:
            rules: Game rules implementation
        """
        self.rules = rules
        self._scores = {}
        self._player_names = []
        self._streaks = {}
        self._use_streaks = False
    
    def initialize_game_session(self, player_1_name: str, player_2_name: str, use_streaks: bool = False):
        """
        Initialize a new game session with player names and scoring type.
        
        Args:
            player_1_name: Name of the first player
            player_2_name: Name of the second player
            use_streaks: If True, use streak-based scoring
        """
        self._player_names = [player_1_name, player_2_name]
        self._scores = {player_1_name: 0, player_2_name: 0}
        self._streaks = {player_1_name: 0, player_2_name: 0}
        self._use_streaks = use_streaks
    
    def validate_move(self, move: GameMove) -> bool:
        """
        Validate if a move is legal according to game rules.
        
        Args:
            move: The move to validate
            
        Returns:
            True if the move is valid, False otherwise
        """
        if move is None:
            return False
        return move in self.rules.get_valid_moves()
    
    def process_round(self, move_1: GameMove, move_2: GameMove) -> Tuple[int, str]:
        """
        Process a round with two moves and return the result.
        
        Args:
            move_1: Move from player 1
            move_2: Move from player 2
            
        Returns:
            Tuple of (round_result, interaction_description)
        """
        if not self.validate_move(move_1) or not self.validate_move(move_2):
            raise ValueError(GameMessages.INVALID_MOVE)
        
        round_result = self.rules.determine_result(move_1, move_2)
        interaction_description = self.rules.get_interaction_description(move_1, move_2)
        
        if self._player_names:  # Only update scores if players are registered
            self._update_scores_for_round(round_result)
        
        return round_result, interaction_description
    
    def determine_result(self, move_1: GameMove, move_2: GameMove) -> int:
        """
        Determine the result of a round without updating scores.
        
        Args:
            move_1: Move from player 1
            move_2: Move from player 2
            
        Returns:
            1 if player 1 wins, -1 if player 2 wins, 0 if draw
        """
        return self.rules.determine_result(move_1, move_2)
    
    def get_interaction_description(self, move_1: GameMove, move_2: GameMove) -> str:
        """
        Get description of the interaction between two moves.
        
        Args:
            move_1: Move from player 1
            move_2: Move from player 2
            
        Returns:
            String describing the interaction
        """
        return self.rules.get_interaction_description(move_1, move_2)
    
    def _update_scores_for_round(self, round_result: int) -> None:
        """
        Update player scores based on round result.
        
        Args:
            round_result: 1 if player 1 wins, -1 if player 2 wins, 0 if draw
        """
        player_1_name = self._player_names[0]
        player_2_name = self._player_names[1]
        
        if self._use_streaks:
            self._update_streak_scores(round_result, player_1_name, player_2_name)
        else:
            self._update_standard_scores(round_result, player_1_name, player_2_name)
    
    def _update_standard_scores(self, round_result: int, player_1_name: str, player_2_name: str):
        """Update scores using standard scoring."""
        if round_result == ScoringConstants.PLAYER_1_WIN:
            self._scores[player_1_name] += ScoringConstants.STANDARD_WIN_POINTS
        elif round_result == ScoringConstants.PLAYER_2_WIN:
            self._scores[player_2_name] += ScoringConstants.STANDARD_WIN_POINTS
        else:
            self._scores[player_1_name] += ScoringConstants.STANDARD_DRAW_POINTS
            self._scores[player_2_name] += ScoringConstants.STANDARD_DRAW_POINTS
    
    def _update_streak_scores(self, round_result: int, player_1_name: str, player_2_name: str):
        """Update scores using streak-based scoring."""
        if round_result == ScoringConstants.PLAYER_1_WIN:
            # Player 1 wins
            self._streaks[player_1_name] += 1
            self._streaks[player_2_name] = 0
            # Award points based on streak length
            if self._streaks[player_1_name] == 1:
                self._scores[player_1_name] += ScoringConstants.STREAK_FIRST_WIN_POINTS
            elif self._streaks[player_1_name] == 2:
                self._scores[player_1_name] += ScoringConstants.STREAK_SECOND_WIN_POINTS
            else:
                self._scores[player_1_name] += ScoringConstants.STREAK_THIRD_PLUS_WIN_POINTS
        elif round_result == ScoringConstants.PLAYER_2_WIN:
            # Player 2 wins
            self._streaks[player_2_name] += 1
            self._streaks[player_1_name] = 0
            # Award points based on streak length
            if self._streaks[player_2_name] == 1:
                self._scores[player_2_name] += ScoringConstants.STREAK_FIRST_WIN_POINTS
            elif self._streaks[player_2_name] == 2:
                self._scores[player_2_name] += ScoringConstants.STREAK_SECOND_WIN_POINTS
            else:
                self._scores[player_2_name] += ScoringConstants.STREAK_THIRD_PLUS_WIN_POINTS
        else:
            # Draw - reset streaks
            self._streaks[player_1_name] = 0
            self._streaks[player_2_name] = 0
            # No points awarded for draws
    
    def get_scores(self) -> dict:
        """Get current score dictionary."""
        return self._scores.copy()
    
    def get_player_score(self, player_name: str) -> float:
        """Get current score for a specific player."""
        return self._scores.get(player_name, 0)
    
    def get_streaks(self) -> dict:
        """Get current streak dictionary."""
        return self._streaks.copy()
    
    def get_player_streak(self, player_name: str) -> int:
        """Get current streak for a specific player."""
        return self._streaks.get(player_name, 0)
    
    def determine_winner(self) -> Tuple[Optional[str], float, float]:
        """
        Determine the winner based on current scores.
        
        Returns:
            Tuple of (winner_name or None if draw, winner_score, loser_score)
        """
        if not self._player_names:
            return None, 0, 0
            
        player_1_name = self._player_names[0]
        player_2_name = self._player_names[1]
        
        player_1_score = self._scores[player_1_name]
        player_2_score = self._scores[player_2_name]
        
        if player_1_score > player_2_score:
            return player_1_name, player_1_score, player_2_score
        elif player_2_score > player_1_score:
            return player_2_name, player_2_score, player_1_score
        else:
            return None, player_1_score, player_2_score  # Draw
    
    def is_series_over(self, win_threshold: int) -> bool:
        """
        Check if a best-of-X series is over.
        
        Args:
            win_threshold: Points needed to win the series
            
        Returns:
            True if the series is over (someone reached the threshold)
        """
        for player_name in self._player_names:
            if self.get_player_score(player_name) >= win_threshold:
                return True
        return False
    
    def reset_scores(self):
        """Reset all scores and streaks while keeping player names."""
        for player_name in self._player_names:
            self._scores[player_name] = 0
            self._streaks[player_name] = 0
