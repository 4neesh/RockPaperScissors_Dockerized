from src.game_utils.game_mode import GameMode
from src.players.player import Player

class GameModeFactory:
    @staticmethod
    def create_players(game: 'Game', mode: GameMode) -> list[Player]:
        return mode.initialise_players_in_game(game) 