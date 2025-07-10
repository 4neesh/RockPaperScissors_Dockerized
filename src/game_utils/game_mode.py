from enum import Enum

from game import Game
from src.players.computer_player import ComputerPlayer
from src.players.human_player import HumanPlayer
from src.players.player import Player
from constants import GameConfig, Messages, UIConfig, ErrorMessages


class GameMode(Enum):
    """
    Enum class to represent different game modes. Each mode defines the number of human and computer players
    involved in the game. The game mode must have exactly 2 players in total (human + computer).
    """

    HUMAN_VS_COMPUTER = (GameConfig.PLAYER_ID_OFFSET, GameConfig.PLAYER_ID_OFFSET)

    def __init__(self, humans: int, computers: int):
        self.humans = humans
        self.computers = computers
        if self.humans + self.computers != GameConfig.REQUIRED_PLAYERS:
            raise ValueError(ErrorMessages.INVALID_GAME_MODE_ERROR.format(
                required_players=GameConfig.REQUIRED_PLAYERS
            ))

    def initialise_players_in_game(self, game: Game) -> [Player, Player]:
        players = []
        for i in range(self.humans):
            players.append(HumanPlayer(game, i + GameConfig.PLAYER_ID_OFFSET))
        for i in range(self.computers):
            players.append(ComputerPlayer(game, i + self.humans + GameConfig.PLAYER_ID_OFFSET))
        return players

    @staticmethod
    def get_game_mode_by_number(index_pos: int) -> "GameMode":
        return list(GameMode)[index_pos - GameConfig.PLAYER_ID_OFFSET]

    @staticmethod
    def formatted_choices() -> list[str]:
        return [Messages.GAME_MODE_FORMAT.format(
            index=index,
            mode_name=mode.name
        ) for index, mode in enumerate(GameMode, start=UIConfig.GAME_MODE_START_INDEX)]