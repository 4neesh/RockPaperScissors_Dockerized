from src.game_utils.hand_gesture import HandGesture
from src.io_utils.output_provider import OutputProvider
from src.players.human_player import HumanPlayer
from src.players.player import Player
from src.constants import GameMessages, DisplayConstants, PlayerConstants


class OutputProviderConsole(OutputProvider):
    """
    An implementation of the OutputProvider class that handles all output
    to the console
    """
    def output_game_mode_error(self):
        print(GameMessages.GAME_MODE_ERROR)

    def output_drawn_round(self, player_1_move: str, player_2_move: str) -> None:
        print(GameMessages.DRAW_ROUND.format(move1=player_1_move, move2=player_2_move))

    def output_game_winner(self, winner: str, winner_score: int, loser_score: int) -> None:
        print(GameMessages.GAME_WINNER.format(
            winner=winner,
            winner_score=winner_score,
            loser_score=loser_score
        ))

    def output_drawn_game(self) -> None:
        print(GameMessages.DRAW_GAME)

    def output_round_description(self, description: str) -> None:
        print(description)

    def output_name_error(self) -> None:
        print(GameMessages.PLAYER_NAME_ERROR.format(max_length=PlayerConstants.MAX_NAME_LENGTH))

    def output_round_number(self, round_number: int, rounds_in_game: int) -> None:
        print(GameMessages.ROUND_HEADER.format(current=round_number, total=rounds_in_game))

    def output_round_moves(self, player_1: Player, player_2: Player, player_1_move: HandGesture, player_2_move: HandGesture) -> None:
        print(GameMessages.ROUND_MOVES.format(
            player1=player_1.get_name(),
            move1=player_1_move,
            player2=player_2.get_name(),
            move2=player_2_move
        ))
        print(DisplayConstants.TABLE_SEPARATOR_CHAR * DisplayConstants.ROUND_SEPARATOR_LENGTH)

    def introduce_game(self, game: str) -> None:
        print(GameMessages.GAME_INTRO.format(game=game))

    def output_scores_table(self, _scores: dict[str, int]) -> None:
        print(f"\n{DisplayConstants.PLAYER_COLUMN_HEADER:<{DisplayConstants.SCORE_TABLE_NAME_WIDTH}}"
              f"{DisplayConstants.SCORE_COLUMN_HEADER:<{DisplayConstants.SCORE_TABLE_SCORE_WIDTH}}")
        print(DisplayConstants.TABLE_SEPARATOR_CHAR * DisplayConstants.SCORE_TABLE_SEPARATOR_LENGTH)
        for name, score in _scores.items():
            print(f"{name:<{DisplayConstants.SCORE_TABLE_NAME_WIDTH}}"
                  f"{score:<{DisplayConstants.SCORE_TABLE_SCORE_WIDTH}}")
        print(DisplayConstants.TABLE_SEPARATOR_CHAR * DisplayConstants.SCORE_TABLE_SEPARATOR_LENGTH)

    def output_rounds_error(self, max_rounds: int) -> None:
        from src.constants import GameConstants
        print(GameMessages.ROUNDS_ERROR.format(
            min=GameConstants.MIN_ROUNDS,
            max=max_rounds
        ))

    def output_gesture_error(self) -> None:
        print(GameMessages.INVALID_GESTURE)

    def output_end_game(self) -> None:
        print(GameMessages.GAME_ENDING)