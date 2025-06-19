from src.game_utils.hand_gesture import HandGesture
from src.io_utils.output_provider import OutputProvider
from src.players.human_player import HumanPlayer
from src.players.player import Player


class OutputProviderConsole(OutputProvider):
    """
    An implementation of the OutputProvider class that handles all output 
    to the console
    """
    def output_game_mode_error(self):
        print(f"Invalid selection. Please enter a number that corresponds to a game mode.")

    def output_drawn_round(self, player_1_move: str, player_2_move: str) -> None:
        print(f"\n{player_1_move} vs {player_2_move} is a draw.")

    def output_game_winner(self, winner: str, winner_score: int, loser_score: int) -> None:
        print(f"\n{winner} won with a score of {winner_score} to {loser_score}")

    def output_drawn_game(self) -> None:
        print("\nThe game is a draw!")

    def output_round_description(self, description: str) -> None:
        print(description)

    def output_name_error(self) -> None:
        print(f"Invalid input. Name cannot be empty and must be shorter than {HumanPlayer.MAX_NAME_LENGTH} characters.")

    def output_round_number(self, round_number: int, rounds_in_game: int) -> None:
        print(f"\nRound {round_number} of {rounds_in_game}")

    def output_round_moves(self, player_1: Player, player_2: Player, player_1_move: HandGesture, player_2_move: HandGesture) -> None:
        print(f"\n{player_1.get_name()} ({player_1_move})  |  {player_2.get_name()} ({player_2_move})")
        print("-" * 50)

    def introduce_game(self, game: str) -> None:
        print(f"We're playing {game}!")

    def output_scores_table(self, _scores: dict[str, int]) -> None:
        print(f"\n{'Player':<20}{'Score':<10}")
        print("-" * 30)
        for name, score in _scores.items():
            print(f"{name:<20}{score:<10}")
        print("-" * 30)

    def output_rounds_error(self, max_rounds: int) -> None:
        print(f"Invalid input. Please enter a valid number between 1 and {max_rounds}.")

    def output_gesture_error(self) -> None:
        print("Invalid input. Please enter a valid Hand Gesture number.")

    def output_end_game(self) -> None:
        print("Game is ending")