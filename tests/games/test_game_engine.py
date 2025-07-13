"""
Tests for the GameEngine class.
"""
import unittest
from unittest.mock import MagicMock

from game_engine import GameEngine
from src.games.rps.rps_rules import RPSRules
from src.games.rps.rps_move import RPSMove
from src.constants import ScoringConstants


class TestGameEngine(unittest.TestCase):
    """Tests for the GameEngine class."""

    def setUp(self):
        """Set up for each test."""
        self.rules = RPSRules()
        self.game_engine = GameEngine(self.rules)
        self.game_engine.initialize_game_session("Player1", "Player2")

    def test_validate_move(self):
        """Test move validation."""
        self.assertTrue(self.game_engine.validate_move(RPSMove.ROCK))
        self.assertTrue(self.game_engine.validate_move(RPSMove.PAPER))
        self.assertTrue(self.game_engine.validate_move(RPSMove.SCISSORS))
        self.assertFalse(self.game_engine.validate_move(None))

        # Create a mock move that's not in the valid moves
        mock_move = MagicMock()
        self.assertFalse(self.game_engine.validate_move(mock_move))

    def test_process_round(self):
        """Test standard round processing."""
        # Rock beats scissors
        result, description = self.game_engine.process_round(RPSMove.ROCK, RPSMove.SCISSORS)
        self.assertEqual(result, ScoringConstants.PLAYER_1_WIN)
        self.assertIn("Rock crushes Scissors", description)

        # Paper beats rock
        result, description = self.game_engine.process_round(RPSMove.ROCK, RPSMove.PAPER)
        self.assertEqual(result, ScoringConstants.PLAYER_2_WIN)
        self.assertIn("Paper covers Rock", description)

        # Draw
        result, description = self.game_engine.process_round(RPSMove.ROCK, RPSMove.ROCK)
        self.assertEqual(result, ScoringConstants.DRAW)
        self.assertIn("Draw", description)

    def test_determine_winner(self):
        """Test determining winner."""
        # Initial state: no winner
        winner, winner_score, loser_score = self.game_engine.determine_winner()
        self.assertIsNone(winner)
        self.assertEqual(winner_score, 0)
        self.assertEqual(loser_score, 0)

        # Player 1 wins a round
        self.game_engine.process_round(RPSMove.ROCK, RPSMove.SCISSORS)
        winner, winner_score, loser_score = self.game_engine.determine_winner()
        self.assertEqual(winner, "Player1")
        self.assertEqual(winner_score, 1)
        self.assertEqual(loser_score, 0)

        # Player 2 wins two rounds
        self.game_engine.process_round(RPSMove.ROCK, RPSMove.PAPER)
        self.game_engine.process_round(RPSMove.ROCK, RPSMove.PAPER)
        winner, winner_score, loser_score = self.game_engine.determine_winner()
        self.assertEqual(winner, "Player2")
        self.assertEqual(winner_score, 2)
        self.assertEqual(loser_score, 1)

        # Draw
        self.game_engine.process_round(RPSMove.ROCK, RPSMove.ROCK)
        self.game_engine.process_round(RPSMove.PAPER, RPSMove.PAPER)
        winner, winner_score, loser_score = self.game_engine.determine_winner()
        self.assertEqual(winner, "Player2")  # Still winning
        self.assertEqual(winner_score, 3)  # 2 + 0.5*2
        self.assertEqual(loser_score, 2)  # 1 + 0.5*2

    def test_streak_scoring(self):
        """Test streak-based scoring."""
        self.game_engine.initialize_game_session("Player1", "Player2", use_streaks=True)

        # Player 1 first win: 1 point
        self.game_engine.process_round(RPSMove.ROCK, RPSMove.SCISSORS)
        self.assertEqual(self.game_engine.get_player_score("Player1"), 1)
        self.assertEqual(self.game_engine.get_player_streak("Player1"), 1)

        # Player 1 second consecutive win: 2 points
        self.game_engine.process_round(RPSMove.ROCK, RPSMove.SCISSORS)
        self.assertEqual(self.game_engine.get_player_score("Player1"), 3)  # 1+2
        self.assertEqual(self.game_engine.get_player_streak("Player1"), 2)

        # Player 1 third consecutive win: 3 points
        self.game_engine.process_round(RPSMove.ROCK, RPSMove.SCISSORS)
        self.assertEqual(self.game_engine.get_player_score("Player1"), 6)  # 1+2+3
        self.assertEqual(self.game_engine.get_player_streak("Player1"), 3)

        # Draw: resets streak
        self.game_engine.process_round(RPSMove.ROCK, RPSMove.ROCK)
        self.assertEqual(self.game_engine.get_player_score("Player1"), 6)  # Unchanged
        self.assertEqual(self.game_engine.get_player_streak("Player1"), 0)

        # Player 2 first win: 1 point
        self.game_engine.process_round(RPSMove.SCISSORS, RPSMove.ROCK)
        self.assertEqual(self.game_engine.get_player_score("Player2"), 1)
        self.assertEqual(self.game_engine.get_player_streak("Player2"), 1)

    def test_is_series_over(self):
        """Test series termination."""
        self.assertFalse(self.game_engine.is_series_over(3))

        # Player 1 wins 3 rounds
        self.game_engine.process_round(RPSMove.ROCK, RPSMove.SCISSORS)
        self.game_engine.process_round(RPSMove.ROCK, RPSMove.SCISSORS)
        self.game_engine.process_round(RPSMove.ROCK, RPSMove.SCISSORS)

        self.assertTrue(self.game_engine.is_series_over(3))
        self.assertFalse(self.game_engine.is_series_over(4))

    def test_reset_scores(self):
        """Test score reset."""
        self.game_engine.process_round(RPSMove.ROCK, RPSMove.SCISSORS)
        self.game_engine.process_round(RPSMove.ROCK, RPSMove.SCISSORS)
        self.game_engine.process_round(RPSMove.SCISSORS, RPSMove.ROCK)

        # Verify some scores exist
        self.assertEqual(self.game_engine.get_player_score("Player1"), 2)
        self.assertEqual(self.game_engine.get_player_score("Player2"), 1)

        # Reset and verify
        self.game_engine.reset_scores()
        self.assertEqual(self.game_engine.get_player_score("Player1"), 0)
        self.assertEqual(self.game_engine.get_player_score("Player2"), 0)


if __name__ == "__main__":
    unittest.main()