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

    def test_score_manager_resets_on_replay(self):
        """
        Test that the score manager starts fresh when the player chooses to replay.
        This test verifies that scores from previous games don't carry over to new games.
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

        # Create a real score manager to test the actual behavior
        score_manager = ScoreManagerFactory.create_score_manager(
            "standard", game, mock_player1.get_name(), mock_player2.get_name()
        )

        # Mock player moves - Player1 always wins
        mock_player1.make_move.return_value = HandGesture.ROCK
        mock_player2.make_move.return_value = HandGesture.SCISSORS

        # Mock play_again_request to return 'y' first time, then 'n' second time
        input_provider.play_again_request.side_effect = ['y', 'n']

        # Mock request_game_option to return "1" (1 round)
        with patch.object(game, 'request_game_option', return_value="1"):
            with patch.object(game, 'exit_game'):
                # Simulate first game - Player1 wins 1 round
                game.play_rounds(1, mock_player1, mock_player2, score_manager)

                # Check scores after first game
                first_game_player1_score = score_manager.get_player_score("Player1")
                first_game_player2_score = score_manager.get_player_score("Player2")

                # Player1 should have 1 point, Player2 should have 0
                self.assertEqual(first_game_player1_score, 1)
                self.assertEqual(first_game_player2_score, 0)

                # Simulate second game (replay) - Player1 wins another round
                game.play_rounds(1, mock_player1, mock_player2, score_manager)

                # Check scores after second game
                second_game_player1_score = score_manager.get_player_score("Player1")
                second_game_player2_score = score_manager.get_player_score("Player2")

                self.assertEqual(second_game_player1_score, 1,
                                 "Score manager should reset between games when replaying")
                self.assertEqual(second_game_player2_score, 0,
                                 "Score manager should reset between games when replaying")

    def test_final_scores_only_reflect_last_game_after_replay(self):
        """
        Test that simulates two players playing, replaying, and verifies that the final scores
        only reflect the last game and not carried over scores from previous games.
        """
        # Setup mocks
        input_provider = Mock(spec=InputProviderConsole)
        output_provider = Mock(spec=OutputProviderConsole)
        game = GamePaperScissorsRock(input_provider, output_provider)

        # Mock player setup
        mock_player1 = Mock(spec=Player)
        mock_player2 = Mock(spec=Player)
        mock_player1.get_name.return_value = "Alice"
        mock_player2.get_name.return_value = "Bob"

        # Create a real score manager to track the actual behavior
        score_manager = ScoreManagerFactory.create_score_manager(
            "standard", game, mock_player1.get_name(), mock_player2.get_name()
        )

        # Mock play_again_request to return 'y' first time, then 'n' second time
        input_provider.play_again_request.side_effect = ['y', 'n']

        # Mock request_game_option to return "3" (3 rounds each game)
        with patch.object(game, 'request_game_option', return_value="3"):
            with patch.object(game, 'exit_game'):
                # First game: Alice wins all 3 rounds (Alice gets 3 points, Bob gets 0)
                mock_player1.make_move.return_value = HandGesture.ROCK
                mock_player2.make_move.return_value = HandGesture.SCISSORS

                # Second game (replay): Bob wins all 3 rounds (Bob should get 3 points, Alice should get 0)
                # We'll change the moves after the first game
                def side_effect_moves_player1():
                    # First 3 calls return ROCK (Alice wins), next 3 calls return SCISSORS (Alice loses)
                    if mock_player1.make_move.call_count <= 3:
                        return HandGesture.ROCK
                    else:
                        return HandGesture.SCISSORS

                def side_effect_moves_player2():
                    # First 3 calls return SCISSORS (Bob loses), next 3 calls return ROCK (Bob wins)
                    if mock_player2.make_move.call_count <= 3:
                        return HandGesture.SCISSORS
                    else:
                        return HandGesture.ROCK

                mock_player1.make_move.side_effect = side_effect_moves_player1
                mock_player2.make_move.side_effect = side_effect_moves_player2

                # Capture the final game result output
                with patch('sys.stdout', new=StringIO()) as captured_output:
                    game.play_game([mock_player1, mock_player2], score_manager)

                # After replay, the final scores should only reflect the last game
                # Bob should have won the last game (3-0), so the final result should show Bob winning
                final_output = captured_output.getvalue()

                # BUG: Currently the scores carry over, so Alice would have 3 points from first game
                # plus 0 from second game = 3 total, and Bob would have 0 + 3 = 3 total (tie)
                # EXPECTED: Only the last game should count, so Bob should win 3-0

                # Check final scores in the score manager
                alice_final_score = score_manager.get_player_score("Alice")
                bob_final_score = score_manager.get_player_score("Bob")

                # The final scores should only reflect the last game
                # Since play_rounds awards 1 point to the overall game winner,
                # Bob should have 1 point (from winning the last game) and Alice should have 0
                self.assertEqual(bob_final_score, 1,
                                 "Bob should have 1 point from winning the last game")
                self.assertEqual(alice_final_score, 0,
                                 "Alice should have 0 points as scores should reset for the replay")

                # BUG: Currently Alice still has 1 point from the first game, making it a tie
                # The actual bug is that Alice's score carries over, so final scores are Alice: 1, Bob: 1

                # Verify the final game result message shows Bob as the winner
                self.assertIn("Bob won", final_output,
                              "Final output should show Bob as the winner of the last game")
                self.assertNotIn("drawn game", final_output.lower(),
                                 "Game should not be drawn if scores are properly reset")
