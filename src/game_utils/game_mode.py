from enum import Enum

from game import Game
from src.players.computer_player import ComputerPlayer
from src.players.human_player import HumanPlayer
from src.players.player import Player
from src.constants import GameConstants, GameMessages


class GameMode(Enum):
    """
    Enum class to represent different game modes. Each mode defines the number of human and computer players
    involved in the game. The game mode must have exactly 2 players in total (human + computer).
    """

    HUMAN_VS_COMPUTER = (1, 1)

    def __init__(self, humans: int, computers: int):
        self.humans = humans
        self.computers = computers
        if self.humans + self.computers != GameConstants.REQUIRED_PLAYER_COUNT:
            raise ValueError(GameMessages.INVALID_GAME_MODE.format(
                count=GameConstants.REQUIRED_PLAYER_COUNT
            ))

    def initialise_players_in_game(self, game: Game) -> [Player, Player]:
        players = []
        for i in range(self.humans):
            players.append(HumanPlayer(game, i + 1))
        for i in range(self.computers):
            players.append(ComputerPlayer(game, i + self.humans + 1))
        return players

    @staticmethod
    def get_game_mode_by_number(index_pos: int) -> "GameMode":
        return list(GameMode)[index_pos - 1]

    @staticmethod
    def formatted_choices() -> list[str]:
        return [GameMessages.GAME_MODE_FORMAT.format(
            index=index,
            mode_name=mode.name
        ) for index, mode in enumerate(GameMode, start=1)]