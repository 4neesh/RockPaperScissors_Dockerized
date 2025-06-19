import unittest
from src.game_utils.score_manager import ScoreManager, StandardScoreManager
from unittest.mock import Mock

class TestScoreManager(unittest.TestCase):

    def test_score_update_single_round(self):
        game = Mock()
        score_manager = StandardScoreManager(game, "Player 1", "Player 2")
        score_manager.update_scores_for_round(1)  # Player 1 wins
        self.assertEqual(score_manager._scores["Player 1"], 1)
        self.assertEqual(score_manager._scores["Player 2"], 0)

    def test_score_tied_round(self):
        game = Mock()
        score_manager = StandardScoreManager(game, "Player 1", "Player 2")
        score_manager.update_scores_for_round(0)  # Tied round
        self.assertEqual(score_manager._scores["Player 1"], 0.5)
        self.assertEqual(score_manager._scores["Player 2"], 0.5)

    def test_multiple_rounds(self):
        game = Mock()
        score_manager = StandardScoreManager(game, "Player 1", "Player 2")
        score_manager.update_scores_for_round(1)  # Player 1 wins
        score_manager.update_scores_for_round(-1) # Player 2 wins
        score_manager.update_scores_for_round(0)  # Tied round
        self.assertEqual(score_manager._scores["Player 1"], 1.5)
        self.assertEqual(score_manager._scores["Player 2"], 1.5)

    def test_game_results_winner(self):
        game = Mock()
        score_manager = StandardScoreManager(game, "Player 1", "Player 2")
        score_manager.update_scores_for_round(1)  # Player 1 wins
        score_manager.update_scores_for_round(1)  # Player 1 wins
        score_manager.return_game_result()
        game.output_provider.output_game_winner.assert_called_with("Player 1", 2, 0)

    def test_game_results_draw(self):
        game = Mock()
        score_manager = StandardScoreManager(game, "Player 1", "Player 2")
        score_manager.update_scores_for_round(1)  # Player 1 wins
        score_manager.update_scores_for_round(-1) # Player 2 wins
        score_manager.return_game_result()
        game.output_provider.output_drawn_game.assert_called_once()
