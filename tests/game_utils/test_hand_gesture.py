import unittest

from src.constants import GameConstants, ScoringConstants
from src.game_utils.hand_gesture import HandGesture
from src.game_utils.rps_rules import RPSRules


class TestHandGesture(unittest.TestCase):

    def test_validate_entry(self):
        self.assertTrue(HandGesture.validate_entry(GameConstants.GESTURE_ROCK))
        self.assertTrue(HandGesture.validate_entry(GameConstants.GESTURE_PAPER))
        self.assertFalse(HandGesture.validate_entry(4))
        self.assertFalse(HandGesture.validate_entry(0))

class TestGestureRules(unittest.TestCase):

    def test_determine_result(self):
        rps = RPSRules()
        self.assertEqual(rps.determine_result(HandGesture.ROCK, HandGesture.SCISSORS), ScoringConstants.PLAYER_1_WIN)
        self.assertEqual(rps.determine_result(HandGesture.PAPER, HandGesture.ROCK), ScoringConstants.PLAYER_1_WIN)
        self.assertEqual(rps.determine_result(HandGesture.SCISSORS, HandGesture.PAPER), ScoringConstants.PLAYER_1_WIN)
        self.assertEqual(rps.determine_result(HandGesture.ROCK, HandGesture.ROCK), ScoringConstants.DRAW)
        self.assertEqual(rps.determine_result(HandGesture.PAPER, HandGesture.SCISSORS), ScoringConstants.PLAYER_2_WIN)

    def test_get_interaction_description(self):
        rps = RPSRules()
        self.assertEqual(rps.get_interaction_description(HandGesture.ROCK, HandGesture.SCISSORS), "Rock blunts Scissors")
        self.assertEqual(rps.get_interaction_description(HandGesture.PAPER, HandGesture.ROCK), "Paper wraps Rock")
        self.assertEqual(rps.get_interaction_description(HandGesture.SCISSORS, HandGesture.PAPER), "Scissors cuts Paper")
        self.assertEqual(rps.get_interaction_description(HandGesture.ROCK, HandGesture.ROCK), "Rock vs Rock is a draw")
        self.assertEqual(rps.get_interaction_description(HandGesture.PAPER, HandGesture.PAPER), "Paper vs Paper is a draw")