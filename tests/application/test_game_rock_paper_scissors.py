import unittest
from unittest.mock import Mock, patch

from game_paper_scissors_rock import GamePaperScissorsRock
from src.io_utils.input_provider_console import InputProviderConsole
from src.io_utils.output_provider_console import OutputProviderConsole
from src.game_utils.game_mode import GameMode
from src.players.player import Player
from src.game_utils.hand_gesture import HandGesture
from io import StringIO
from src.game_utils.score_manager_factory import ScoreManagerFactory

class TestGamePaperScissorsRock(unittest.TestCase):

    def test_select_game_mode_human_vs_computer(self):
        input_provider = Mock(spec=InputProviderConsole)
        output_provider = OutputProviderConsole()
        game = GamePaperScissorsRock(input_provider, output_provider)
        input_provider.game_mode_request.return_value = '1'
        selected_mode = game.select_game_mode()
        self.assertEqual(selected_mode, GameMode.HUMAN_VS_COMPUTER)

    @patch('sys.exit')
    def test_game_exit_when_replay_declined(self, mock_exit):
        # Setup mocks
        input_provider = Mock(spec=InputProviderConsole)
        output_provider = OutputProviderConsole()
        game = GamePaperScissorsRock(input_provider, output_provider)

        # Mock game mode selection
        input_provider.game_mode_request.return_value = '1'  # Human vs Computer

        # Mock player setup
        mock_player1 = Mock(spec=Player)
        mock_player2 = Mock(spec=Player)
        mock_player1.get_name.return_value = "Player 1"
        mock_player2.get_name.return_value = "Player 2"

        # Mock the game mode to return our mock players
        mock_game_mode = Mock()
        mock_game_mode.initialise_players_in_game.return_value = [mock_player1, mock_player2]

        # Mock select_game_mode to return our mock game mode
        game.select_game_mode = Mock(return_value=mock_game_mode)

        # Mock game option request
        game.request_game_option = Mock(return_value="1")  # 1 round

        # Mock player moves
        mock_player1.make_move.return_value = "rock"
        mock_player2.make_move.return_value = "scissors"

        # Mock score manager
        mock_score_manager = Mock()

        # Mock play_rounds to avoid actual gameplay
        game.play_rounds = Mock()

        # Mock play_again_request to return 'n' (no replay)
        input_provider.play_again_request.return_value = 'n'

        # Call start_game
        with patch('src.game_utils.score_manager_factory.ScoreManagerFactory.create_score_manager',
                   return_value=mock_score_manager):
            game.start_game()

        # Verify that exit_game was called
        mock_exit.assert_called_once_with(0)

    @patch('sys.exit')
    def test_best_of_five_result_returned(self, mock_exit):
        # Setup mocks
        input_provider = Mock(spec=InputProviderConsole)
        output_provider = OutputProviderConsole()
        game = GamePaperScissorsRock(input_provider, output_provider)

        # Mock game mode selection
        input_provider.game_mode_request.return_value = '1'  # Human vs Computer

        # Mock player setup
        mock_player1 = Mock(spec=Player)
        mock_player2 = Mock(spec=Player)
        mock_player1.get_name.return_value = "Player 1"
        mock_player2.get_name.return_value = "Player 2"

        # Mock the game mode to return our mock players
        mock_game_mode = Mock()
        mock_game_mode.initialise_players_in_game.return_value = [mock_player1, mock_player2]

        # Mock select_game_mode to return our mock game mode
        game.select_game_mode = Mock(return_value=mock_game_mode)

        # Mock game option request
        game.request_game_option = Mock(return_value="bo5")  # best of five

        # Mock player moves to have player1 win (rock beats scissors)
        mock_player1.make_move.return_value = HandGesture.ROCK
        mock_player2.make_move.return_value = HandGesture.SCISSORS

        # Use real score manager and output provider to capture actual prints
        score_manager = ScoreManagerFactory.create_score_manager(
            "standard", game, mock_player1.get_name(), mock_player2.get_name()
        )

        with patch('sys.stdout', new=StringIO()) as game_score_out:
            game.play_game([mock_player1, mock_player2], score_manager)
            score_manager.return_game_result()

        # Assert for the game result message
        expected_game_message = "\nPlayer 1 won with a score of 3 to 0"
        unexpected_game_message = "\nPlayer 1 won with a score of 1 to 0"
        self.assertIn(expected_game_message, game_score_out.getvalue())
        self.assertNotIn(unexpected_game_message, game_score_out.getvalue())
