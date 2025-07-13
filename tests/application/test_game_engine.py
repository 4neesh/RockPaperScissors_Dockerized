"""
Unit tests for the GameEngine class.

This module tests the core functionality of the GameEngine,
including move validation, result determination, and score tracking.
"""

import unittest
from unittest.mock import Mock, patch

from src.games.rps.rps_rules import RPSRules
from src.games.rps.rps_move import RPSMove
from src.constants import ScoringConstants
from game_engine import GameEngine


class TestGameEngine(unittest.TestCase):
    """
    Test suite for the GameEngine class.
    """
    
    def setUp(self):
        """Set up test fixtures."""
        self.output_provider = Mock()
        self.rules = RPSRules()
        self.engine = GameEngine(self.rules, self.output_provider)
        
    def test_validate_game_option(self):
        """Test game option validation."""
        # Test valid inputs
        self.assertTrue(self.engine.validate_game_option("bo5", 10))
        self.assertTrue(self.engine.validate_game_option("1", 10))
        self.assertTrue(self.engine.validate_game_option("5", 10))
        self.assertTrue(self.engine.validate_game_option("10", 10))
        
        # Test invalid inputs
        self.assertFalse(self.engine.validate_game_option("0", 10))
        self.assertFalse(self.engine.validate_game_option("11", 10))
        self.assertFalse(self.engine.validate_game_option("abc", 10))
        self.assertFalse(self.engine.validate_game_option("", 10))
        
    def test_determine_round_result(self):
        """Test round result determination via rules."""
        # Rock vs Scissors (Rock wins)
        move_1 = RPSMove.ROCK
        move_2 = RPSMove.SCISSORS
        result = self.rules.determine_result(move_1, move_2)
        self.assertEqual(result, ScoringConstants.PLAYER_1_WIN)
        
        # Paper vs Rock (Paper wins)
        move_1 = RPSMove.PAPER
        move_2 = RPSMove.ROCK
        result = self.rules.determine_result(move_1, move_2)
        self.assertEqual(result, ScoringConstants.PLAYER_1_WIN)
        
        # Scissors vs Paper (Scissors wins)
        move_1 = RPSMove.SCISSORS
        move_2 = RPSMove.PAPER
        result = self.rules.determine_result(move_1, move_2)
        self.assertEqual(result, ScoringConstants.PLAYER_1_WIN)
        
        # Rock vs Rock (Draw)
        move_1 = RPSMove.ROCK
        move_2 = RPSMove.ROCK
        result = self.rules.determine_result(move_1, move_2)
        self.assertEqual(result, ScoringConstants.DRAW)
        
    @patch('builtins.print')
    def test_handle_timeout(self, mock_print):
        """Test timeout handling."""
        player_1 = Mock()
        player_2 = Mock()
        score_manager = Mock()
        
        player_1.get_name.return_value = "Player 1"
        player_2.get_name.return_value = "Player 2"
        
        # Both players timeout
        result, score_update = self.engine._handle_timeout(
            player_1, player_2, None, None, score_manager
        )
        self.assertEqual(result, "both_timeout")
        self.assertEqual(score_update, ScoringConstants.DRAW)
        
        # Player 1 timeout
        result, score_update = self.engine._handle_timeout(
            player_1, player_2, None, RPSMove.ROCK, score_manager
        )
        self.assertEqual(result, "player_1_timeout")
        self.assertEqual(score_update, ScoringConstants.PLAYER_2_WIN)
        
        # Player 2 timeout
        result, score_update = self.engine._handle_timeout(
            player_1, player_2, RPSMove.ROCK, None, score_manager
        )
        self.assertEqual(result, "player_2_timeout")
        self.assertEqual(score_update, ScoringConstants.PLAYER_1_WIN)
        
        # Both valid
        result, score_update = self.engine._handle_timeout(
            player_1, player_2, RPSMove.ROCK, RPSMove.PAPER, score_manager
        )
        self.assertEqual(result, "both_valid")
        self.assertIsNone(score_update)
        
    def test_process_valid_moves(self):
        """Test processing of valid moves."""
        player_1 = Mock()
        player_2 = Mock()
        move_1 = RPSMove.ROCK
        move_2 = RPSMove.SCISSORS
        score_manager = Mock()
        
        # Call the method
        self.engine._process_valid_moves(player_1, player_2, move_1, move_2, score_manager)
        
        # Verify that the output provider methods were called
        self.output_provider.output_round_moves.assert_called_once_with(
            player_1, player_2, move_1, move_2
        )
        self.output_provider.output_round_description.assert_called_once()
        
        # Verify that the score manager methods were called
        score_manager.update_scores_for_round.assert_called_once_with(ScoringConstants.PLAYER_1_WIN)
        score_manager.return_leaderboard.assert_called_once()


if __name__ == '__main__':
    unittest.main()
