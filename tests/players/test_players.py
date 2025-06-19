import unittest

from src.game_utils.hand_gesture import HandGesture
from src.players.computer_player import ComputerPlayer
from unittest.mock import Mock

class TestPlayers(unittest.TestCase):

    def test_computer_player_move(self):
        game = Mock()
        computer_player = ComputerPlayer(game, 1)
        move = computer_player.make_move()
        self.assertIn(move, [HandGesture.ROCK, HandGesture.PAPER, HandGesture.SCISSORS])

    def test_validate_entry_valid(self):
        self.assertTrue(HandGesture.validate_entry(1), "1 should be a valid move (Rock)")
        self.assertTrue(HandGesture.validate_entry(2), "2 should be a valid move (Paper)")
        self.assertTrue(HandGesture.validate_entry(3), "3 should be a valid move (Scissors)")

    def test_validate_entry_invalid(self):
        self.assertFalse(HandGesture.validate_entry(0), "0 should not be a valid move")
        self.assertFalse(HandGesture.validate_entry(4), "4 should not be a valid move")
        self.assertFalse(HandGesture.validate_entry(-1), "-1 should not be a valid move")

