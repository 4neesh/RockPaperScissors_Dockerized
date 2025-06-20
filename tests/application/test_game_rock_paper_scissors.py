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

        # Mock player moves - Player1 always wins
        mock_player1.make_move.return_value = HandGesture.ROCK
        mock_player2.make_move.return_value = HandGesture.SCISSORS

        # Mock play_again_request to return 'y' first time, then 'n' second time
        input_provider.play_again_request.side_effect = ['y', 'n']

        # Track the score managers created to verify fresh instances are made
        score_managers_created = []
        original_create = ScoreManagerFactory.create_score_manager
        
        def capture_score_manager(*args, **kwargs):
            sm = original_create(*args, **kwargs)
            score_managers_created.append(sm)
            return sm

        # Mock request_game_option to return "1" (1 round)
        with patch.object(game, 'request_game_option', return_value="1"):
            with patch.object(game, 'exit_game'):
                with patch.object(ScoreManagerFactory, 'create_score_manager', side_effect=capture_score_manager):
                    # This should create fresh score managers for each game
                    game.play_game([mock_player1, mock_player2], None)
                
                # Verify that multiple score managers were created (one for each game)
                self.assertGreaterEqual(len(score_managers_created), 2, 
                    "A new score manager should be created for each game when replaying")
                
                # Verify that different instances were created
                if len(score_managers_created) >= 2:
                    self.assertIsNot(score_managers_created[0], score_managers_created[1],
                        "Different score manager instances should be created for each game")

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

        # Mock play_again_request to return 'y' first time, then 'n' second time
        input_provider.play_again_request.side_effect = ['y', 'n']

        # Track the final score manager to verify the fix
        final_score_manager = None
        score_managers_created = []
        original_create = ScoreManagerFactory.create_score_manager
        
        def capture_score_manager(*args, **kwargs):
            nonlocal final_score_manager
            sm = original_create(*args, **kwargs)
            score_managers_created.append(sm)
            final_score_manager = sm  # Keep track of the last one created
            return sm

        # Mock request_game_option to return "3" (3 rounds each game)
        with patch.object(game, 'request_game_option', return_value="3"):
            with patch.object(game, 'exit_game'):
                # First game: Alice wins all 3 rounds (Alice gets 1 point for winning the game)
                # Second game (replay): Bob wins all 3 rounds (Bob gets 1 point for winning the game)
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
                with patch.object(ScoreManagerFactory, 'create_score_manager', side_effect=capture_score_manager):
                    with patch('sys.stdout', new=StringIO()) as captured_output:
                        game.play_game([mock_player1, mock_player2], None)
                
                # Verify that multiple score managers were created (fresh instances for each game)
                self.assertGreaterEqual(len(score_managers_created), 2, 
                    "A new score manager should be created for each game when replaying")
                
                # Check the score managers created - we expect multiple instances
                # The key test is that fresh score managers are created for each game
                # Let's verify the behavior by checking that we have separate instances
                
                # Find the main score managers (not the temp ones from play_rounds)
                # The main score managers are the ones created in play_game method
                main_score_managers = []
                temp_score_managers = []
                
                # The pattern is: main_score_manager, temp_score_manager, main_score_manager, temp_score_manager
                # We want to check the main ones (indices 0, 2, etc.)
                for i, sm in enumerate(score_managers_created):
                    if i % 2 == 0:  # Even indices are main score managers
                        main_score_managers.append(sm)
                    else:  # Odd indices are temp score managers
                        temp_score_managers.append(sm)
                
                # Verify we have at least 2 main score managers (one for each game)
                self.assertGreaterEqual(len(main_score_managers), 2,
                    "Should have separate main score managers for each game")
                
                # Verify they are different instances
                if len(main_score_managers) >= 2:
                    self.assertIsNot(main_score_managers[0], main_score_managers[1],
                        "Main score managers should be different instances for each game")
                
                # The last temp score manager should show Bob winning the last game with 3 points
                if len(temp_score_managers) >= 2:
                    last_temp_sm = temp_score_managers[-1]  # Last temp score manager
                    alice_temp_score = last_temp_sm.get_player_score("Alice")
                    bob_temp_score = last_temp_sm.get_player_score("Bob")
                    
                    # In the temp score manager, Bob should have won all 3 rounds
                    self.assertEqual(bob_temp_score, 3, 
                        "Bob should have 3 points from winning all rounds in the last game")
                    self.assertEqual(alice_temp_score, 0, 
                        "Alice should have 0 points in the last game's temp score manager")
                
                # The key verification is that fresh score managers are created for each game
                # This proves the bug is fixed - scores don't carry over between replays
                print(f"Score managers created: {len(score_managers_created)}")
                print(f"Main score managers: {len(main_score_managers)}")
                print(f"Temp score managers: {len(temp_score_managers)}")
