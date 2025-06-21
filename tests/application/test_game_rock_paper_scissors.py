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
            game.play_game([mock_player1, mock_player2])
            score_manager.return_game_result()

        # Assert for the game result message
        expected_game_message = "\nPlayer 1 won with a score of 3 to 0"
        unexpected_game_message = "\nPlayer 1 won with a score of 1 to 0"
        self.assertIn(expected_game_message, game_score_out.getvalue())
        self.assertNotIn(unexpected_game_message, game_score_out.getvalue())

    def test_best_of_five_three_half_points(self):
        """
        Test a specific best of five game scenario:
        - Round 1: Player 1 chooses rock, Player 2 chooses paper (Player 2 wins)
        - Round 2: Player 1 chooses rock, Player 2 chooses paper (Player 2 wins)
        - Round 3: Both choose none (draw - both get 0.5 points)
        - Round 4: Player 1 chooses rock, Player 2 chooses paper (Player 2 wins)
        - Final score should be 3.5 to 0.5
        """
        # Setup mocks
        input_provider = Mock(spec=InputProviderConsole)
        output_provider = Mock(spec=OutputProviderConsole)
        game = GamePaperScissorsRock(input_provider, output_provider)

        # Mock player setup
        mock_player1 = Mock(spec=Player)
        mock_player2 = Mock(spec=Player)
        mock_player1.get_name.return_value = "Player1"
        mock_player2.get_name.return_value = "Player2"

        # Create a real score manager to track the actual behavior
        score_manager = ScoreManagerFactory.create_score_manager(
            "standard", game, mock_player1.get_name(), mock_player2.get_name()
        )

        # Mock player moves for the specific scenario
        # Round 1 & 2: Player1 rock, Player2 paper (Player2 wins both)
        # Round 3: Both return None (simulating draw)
        # Round 4: Player1 rock, Player2 paper (Player2 wins)
        player1_moves = [HandGesture.ROCK, HandGesture.ROCK, None, HandGesture.ROCK]
        player2_moves = [HandGesture.PAPER, HandGesture.PAPER, None, HandGesture.PAPER]
        
        mock_player1.make_move.side_effect = player1_moves
        mock_player2.make_move.side_effect = player2_moves

        # Mock play_again_request to return 'n' (no replay)
        input_provider.play_again_request.return_value = 'n'

        # Capture the final game result output
        with patch('sys.stdout', new=StringIO()) as captured_output:
            # Simulate the best of 5 game manually
            game.play_best_of_5(mock_player1, mock_player2, score_manager)
            score_manager.return_game_result()

        # Check final scores
        player1_final_score = score_manager.get_player_score("Player1")
        player2_final_score = score_manager.get_player_score("Player2")

        # Assert the expected final scores: Player2 should have 3.5, Player1 should have 0.5
        self.assertEqual(0.5, player1_final_score,  "Player1 should have 0.5 points")
        self.assertEqual(3.5, player2_final_score, "Player2 should have 3.5 points")

    def test_best_of_five_three_none_scenario(self):
        """
        Test a specific best of five game scenario:
        - Round 1: Player 1 chooses rock, Player 2 chooses paper (Player 2 wins)
        - Round 2: Player 1 chooses rock, Player 2 chooses paper (Player 2 wins)
        - Round 3: Both choose none (draw - both get 0.5 points)
        - Round 4: Player 1 chooses rock, Player 2 chooses paper (Player 2 wins)
        - Final score should be 3.5 to 0.5
        """
        # Setup mocks
        input_provider = Mock(spec=InputProviderConsole)
        output_provider = Mock(spec=OutputProviderConsole)
        game = GamePaperScissorsRock(input_provider, output_provider)

        # Mock player setup
        mock_player1 = Mock(spec=Player)
        mock_player2 = Mock(spec=Player)
        mock_player1.get_name.return_value = "Player1"
        mock_player2.get_name.return_value = "Player2"

        # Create a real score manager to track the actual behavior
        score_manager = ScoreManagerFactory.create_score_manager(
            "standard", game, mock_player1.get_name(), mock_player2.get_name()
        )

        # Mock player moves for the specific scenario
        # Round 1 & 2: Player1 rock, Player2 paper (Player2 wins both)
        # Round 3: Both return None (simulating draw)
        # Round 4: Player1 rock, Player2 paper (Player2 wins)
        player1_moves = [HandGesture.ROCK, None, HandGesture.ROCK, HandGesture.ROCK, HandGesture.ROCK]
        player2_moves = [None, HandGesture.PAPER, HandGesture.PAPER, HandGesture.PAPER, HandGesture.PAPER]

        mock_player1.make_move.side_effect = player1_moves
        mock_player2.make_move.side_effect = player2_moves

        # Mock play_again_request to return 'n' (no replay)
        input_provider.play_again_request.return_value = 'n'

        # Capture the final game result output
        with patch('sys.stdout', new=StringIO()) as captured_output:
            # Simulate the best of 5 game manually
            game.play_best_of_5(mock_player1, mock_player2, score_manager)
            score_manager.return_game_result()

        # Check final scores
        player1_final_score = score_manager.get_player_score("Player1")
        player2_final_score = score_manager.get_player_score("Player2")

        # Assert the expected final scores: Player2 should have 3.5, Player1 should have 0.5
        self.assertEqual(1, player1_final_score, "Player1 should have 1 point")
        self.assertEqual(3, player2_final_score, "Player2 should have 3 points")


    def test_play_rounds_both_players_none_should_update_score_with_draw(self):
        """
        Test that when both players return None in play_rounds,
        the score is updated with a draw (0) result.
        This test verifies the bug fix for lines 169-170 in game_paper_scissors_rock.py
        """
        # Setup mocks
        input_provider = Mock(spec=InputProviderConsole)
        output_provider = Mock(spec=OutputProviderConsole)
        game = GamePaperScissorsRock(input_provider, output_provider)

        # Mock player setup
        mock_player1 = Mock(spec=Player)
        mock_player2 = Mock(spec=Player)
        mock_player1.get_name.return_value = "Player1"
        mock_player2.get_name.return_value = "Player2"

        # Create a real score manager to track the actual behavior
        score_manager = ScoreManagerFactory.create_score_manager(
            "standard", game, mock_player1.get_name(), mock_player2.get_name()
        )

        # Mock both players to return None (simulating timeout/no response)
        mock_player1.make_move.return_value = None
        mock_player2.make_move.return_value = None

        # Play 1 round where both players return None
        with patch('sys.stdout', new=StringIO()):
            game.play_rounds(1, mock_player1, mock_player2, score_manager)

        # Check that scores were updated with draw result (0.5 points each)
        player1_score = score_manager.get_player_score("Player1")
        player2_score = score_manager.get_player_score("Player2")

        # Both players should have 0.5 points from the draw
        self.assertEqual(0.5, player1_score, "Player1 should have 0.5 points from draw")
        self.assertEqual(0.5, player2_score, "Player2 should have 0.5 points from draw")
