from src.games.rps.rps_move import RPSMove
from src.players.player import Player
from game import Game
from src.constants import PlayerConstants


class ComputerPlayer(Player):
    """
    Represents a computer-controlled player in the game.
    The computer randomly selects a move for its turn.
    """
    def __init__(self, game: Game, player_id: int):
        name = f"{PlayerConstants.COMPUTER_NAME_PREFIX} {player_id}"
        super().__init__(name)
        self._game = game

    def make_move(self) -> RPSMove:
        return RPSMove.get_random_move()