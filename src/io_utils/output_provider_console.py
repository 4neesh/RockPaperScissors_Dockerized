from src.game_utils.hand_gesture import HandGesture
from src.io_utils.output_provider import OutputProvider
from src.players.player import Player
from constants import Messages, UIConfig, GameConfig


class OutputProviderConsole(OutputProvider):
    """
    An implementation of the OutputProvider class that handles all output
    to the console
    """
    def output_game_mode_error(self):
        print(Messages.GAME_MODE_ERROR)

    def output_drawn_round(self, player_1_move: str, player_2_move: str) -> None:
        print(Messages.DRAW_DESCRIPTION_FORMAT.format(move1=player_1_move, move2=player_2_move))

    def output_game_winner(self, winner: str, winner_score: int, loser_score: int) -> None:
        print(Messages.GAME_WIN_FORMAT.format(
            winner=winner,
            winner_score=winner_score,
            loser_score=loser_score
        ))

    def output_drawn_game(self) -> None:
        print(Messages.GAME_DRAW)

    def output_round_description(self, description: str) -> None:
        print(description)

    def output_name_error(self) -> None:
        print(Messages.NAME_ERROR.format(max_length=GameConfig.MAX_NAME_LENGTH))

    def output_round_number(self, round_number: int, rounds_in_game: int) -> None:
        print(Messages.ROUND_FORMAT.format(
            round_number=round_number,
            total_rounds=rounds_in_game
        ))

    def output_round_moves(self, player_1: Player, player_2: Player, player_1_move: HandGesture, player_2_move: HandGesture) -> None:
        print(Messages.MOVES_FORMAT.format(
            player1_name=player_1.get_name(),
            player1_move=player_1_move,
            player2_name=player_2.get_name(),
            player2_move=player_2_move
        ))
        print(Messages.MOVES_SEPARATOR)

    def introduce_game(self, game: str) -> None:
        print(Messages.GAME_INTRO_FORMAT.format(game_name=game))

    def output_scores_table(self, _scores: dict[str, int]) -> None:
        print(Messages.SCORE_ROW_FORMAT.format(
            name=Messages.PLAYER_HEADER,
            score=Messages.SCORE_HEADER,
            name_width=UIConfig.PLAYER_COLUMN_WIDTH,
            score_width=UIConfig.SCORE_COLUMN_WIDTH
        ))
        print(Messages.TABLE_SEPARATOR)
        for name, score in _scores.items():
            print(Messages.SCORE_ROW_FORMAT.format(
                name=name,
                score=score,
                name_width=UIConfig.PLAYER_COLUMN_WIDTH,
                score_width=UIConfig.SCORE_COLUMN_WIDTH
            ))
        print(Messages.TABLE_SEPARATOR)

    def output_rounds_error(self, max_rounds: int) -> None:
        print(Messages.ROUNDS_ERROR.format(max_rounds=max_rounds))

    def output_gesture_error(self) -> None:
        print(Messages.GESTURE_ERROR)

    def output_end_game(self) -> None:
        print(Messages.GAME_ENDING)