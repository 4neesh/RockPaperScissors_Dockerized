import sys

from src.game_utils.game_mode import GameMode
from src.io_utils.input_provider import InputProvider
from src.io_utils.output_provider import OutputProvider
from src.game_utils.hand_gesture import HandGesture
from src.game_utils.game_rules_factory import GameRulesFactory
from src.players.player import Player
from src.game_utils.score_manager import ScoreManager
from src.game_utils.score_manager_factory import ScoreManagerFactory
from src.io_utils.output_provider_console import OutputProviderConsole
from src.io_utils.input_provider_console import InputProviderConsole
from game import Game
from src.game_factory import GameFactory


class GamePaperScissorsRock(Game):
    """
    Rock, Paper, Scissors game implementation.

    This module defines the GamePaperScissorsRock class, which represents the core logic of the game,
    including player interactions, game flow, scoring, and user I/O.

    Classes:
        GamePaperScissorsRock - Main class handling the gameplay logic for Rock, Paper, Scissors.

    Usage:
        Run this module directly to play the game via the console.
    """

    MAX_ROUNDS = 99
    GAME_TYPE = "rps"
    SCORE_MANAGER_TYPE = "standard"
    MOVE_TIME_LIMIT = 10  # Time limit in seconds for each move
    BEST_OF_5 = 5  # Constant for Best of 5 mode

    @classmethod
    def register(cls):
        """
        Register this game with the GameFactory.
        This method should be called during application initialization.
        """
        GameFactory.register_game(cls.GAME_TYPE, cls)

    def __init__(self, input_prov: InputProvider, output_prov: OutputProvider):
        super().__init__(input_prov, output_prov)
        self.rules = GameRulesFactory.create_rules(self.GAME_TYPE)

    def start_game(self):
        self.output_provider.introduce_game("Paper Scissors Rock")
        game_mode = self.select_game_mode()
        players = game_mode.initialise_players_in_game(self)
        self.play_game(players)  # Removed score_manager creation and passing

    def play_game(self, players: [Player, Player]):
        """
        Play a game with the specified players and score manager.

        Args:
            players: A list of two players (player 1 and player 2)
        """
        replay = "y"
        while replay.lower() == "y":
            # Create a new score manager for each game to reset scores
            score_manager = ScoreManagerFactory.create_score_manager(
                self.SCORE_MANAGER_TYPE,
                self,
                players[0].get_name(),
                players[1].get_name()
            )

            game_option = self.request_game_option()

            if game_option == "bo5":
                # Best of 5 mode
                self.play_best_of_5(players[0], players[1], score_manager)
            else:
                # Standard mode
                rounds_to_play = int(game_option)
                self.play_rounds(rounds_to_play, players[0], players[1], score_manager)

            score_manager.return_game_result()
            replay = self.input_provider.play_again_request()
        self.exit_game()

    def play_best_of_5(self, player_1: Player, player_2: Player, score_manager: ScoreManager):
        """
        Play a best of 5 series between two players.

        Args:
            player_1: The first player
            player_2: The second player
            score_manager: The score manager to use for tracking scores
        """
        round_number = 1

        # Best of 5 means first to 3 points
        while round_number <= self.BEST_OF_5 and score_manager.get_player_score(
                player_1.get_name()) < 3 and score_manager.get_player_score(player_2.get_name()) < 3:
            self.output_provider.output_round_number(round_number, self.BEST_OF_5)
            # Get moves from players with time limit
            player_1_move = player_1.make_move()
            player_2_move = player_2.make_move()

            # Handle timeout cases
            if player_1_move is None and player_2_move is None:
                # Both players timed out, round is a draw
                print("\nBoth players took too long to respond. Round is a draw!")
                score_manager.update_scores_for_round(0)
                score_manager.return_leaderboard()
                round_number += 1
                continue
            elif player_1_move is None:
                # Player 1 timed out, Player 2 wins
                print(f"\n{player_1.get_name()} took too long to respond. {player_2.get_name()} wins this round!")
                score_manager.update_scores_for_round(-1)  # Player 2 wins
                score_manager.return_leaderboard()
                round_number += 1
                continue
            elif player_2_move is None:
                # Player 2 timed out, Player 1 wins
                print(f"\n{player_2.get_name()} took too long to respond. {player_1.get_name()} wins this round!")
                score_manager.update_scores_for_round(1)  # Player 1 wins
                score_manager.return_leaderboard()
                round_number += 1
                continue

            # Normal case - both players made valid moves
            self.output_provider.output_round_moves(player_1, player_2, player_1_move, player_2_move)

            # Use the rules object for interaction description
            interaction_description = self.rules.get_interaction_description(player_1_move, player_2_move)
            self.output_provider.output_round_description(interaction_description)

            # Use the rules object to determine the result
            round_result = self.rules.determine_result(player_1_move, player_2_move)
            score_manager.update_scores_for_round(round_result)
            score_manager.return_leaderboard()
            round_number += 1

        # Provide feedback about best-of-5 result
        if score_manager.get_player_score(player_1.get_name()) > score_manager.get_player_score(player_2.get_name()):
            print(f"\n{player_1.get_name()} wins the Best of 5 series!")
        elif score_manager.get_player_score(player_2.get_name()) > score_manager.get_player_score(player_1.get_name()):
            print(f"\n{player_2.get_name()} wins the Best of 5 series!")
        else:
            print(f"Best of 5 series finishes in a draw!")

    def play_rounds(self, rounds_in_game: int, player_1: Player, player_2: Player, score_manager: ScoreManager):
        """
        Play a specified number of rounds between two players.

        Args:
            rounds_in_game: The number of rounds to play
            player_1: The first player
            player_2: The second player
            score_manager: The score manager to use for tracking scores
        """
        for round_number in range(1, int(rounds_in_game) + 1):
            self.output_provider.output_round_number(round_number, rounds_in_game)

            # Get moves from players with time limit
            player_1_move = player_1.make_move()
            player_2_move = player_2.make_move()

            # Handle timeout cases
            if player_1_move is None and player_2_move is None:
                # Both players timed out, round is a draw
                print("\nBoth players took too long to respond. Round is a draw!")
                score_manager.return_leaderboard()
                continue
            elif player_1_move is None:
                # Player 1 timed out, Player 2 wins
                print(f"\n{player_1.get_name()} took too long to respond. {player_2.get_name()} wins this round!")
                score_manager.update_scores_for_round(-1)  # Player 2 wins
                score_manager.return_leaderboard()
                continue
            elif player_2_move is None:
                # Player 2 timed out, Player 1 wins
                print(f"\n{player_2.get_name()} took too long to respond. {player_1.get_name()} wins this round!")
                score_manager.update_scores_for_round(1)  # Player 1 wins
                score_manager.return_leaderboard()
                continue

            # Normal case - both players made valid moves
            self.output_provider.output_round_moves(player_1, player_2, player_1_move, player_2_move)

            # Use the rules object for interaction description
            interaction_description = self.rules.get_interaction_description(player_1_move, player_2_move)
            self.output_provider.output_round_description(interaction_description)

            # Use the rules object to determine the result
            round_result = self.rules.determine_result(player_1_move, player_2_move)
            score_manager.update_scores_for_round(round_result)
            score_manager.return_leaderboard()

    def request_game_option(self) -> str:
        """
        Request the game option from the user, which can be either a number of rounds
        or 'bo5' for "Best of 5" mode.

        Returns:
            str: Either a number of rounds to play (as a string) or "bo5"
        """
        prompt = f"Enter number of rounds to play (1-{self.MAX_ROUNDS}) or 'bo5' for Best of 5 mode: "
        game_option = input(prompt).strip().lower()

        # Check if it's the Best of 5 option
        if game_option == "bo5":
            return game_option

        # Otherwise validate as regular rounds input
        while not self.is_valid_rounds(game_option):
            game_option = input(prompt).strip().lower()
            if game_option == "bo5":
                return game_option

        return game_option

    def is_valid_rounds(self, rounds_to_play: str) -> bool:
        """Helper method to validate the rounds input."""
        if rounds_to_play.isdigit():
            rounds = int(rounds_to_play)
            if 0 < rounds <= GamePaperScissorsRock.MAX_ROUNDS:
                return True
        self.output_provider.output_rounds_error(GamePaperScissorsRock.MAX_ROUNDS)
        return False

    def select_game_mode(self):
        while True:
            game_mode = self.input_provider.game_mode_request()
            if game_mode.isdigit():
                game_mode_number = int(game_mode)
                if 1 <= game_mode_number <= len(GameMode):
                    return GameMode.get_game_mode_by_number(game_mode_number)
                else:
                    self.output_provider.output_game_mode_error()
            else:
                self.output_provider.output_game_mode_error()

    def exit_game(self):
        self.output_provider.output_end_game()
        sys.exit(0)


if __name__ == "__main__":
    # Register the game with the factory
    GamePaperScissorsRock.register()

    input_provider = InputProviderConsole()
    output_provider = OutputProviderConsole()

    # Create the game using the factory
    rps = GameFactory.create_game(GamePaperScissorsRock.GAME_TYPE, input_provider, output_provider)

    rps.start_game()