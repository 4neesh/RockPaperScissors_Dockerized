from typing import Type, Dict

from game import Game
from src.io_utils.input_provider import InputProvider
from src.io_utils.output_provider import OutputProvider
from src.constants import GameMessages


class GameFactory:
    """
    Factory class for creating game instances.

    This factory manages the creation of different game types and ensures
    that appropriate input/output providers are used for each game.
    """

    _games_registry: Dict[str, Type[Game]] = {}

    @classmethod
    def create_game(cls, game_type: str, input_provider: InputProvider, output_provider: OutputProvider) -> Game:
        """
        Create a game instance of the specified type.

        Args:
            game_type: The type of game to create
            input_provider: Provider for handling input
            output_provider: Provider for handling output

        Returns:
            An instance of the requested game type

        Raises:
            ValueError: If the game type is not supported
        """
        if game_type not in cls._games_registry:
            raise ValueError(GameMessages.UNSUPPORTED_GAME_TYPE.format(game_type=game_type))

        game_class = cls._games_registry[game_type]
        return game_class(input_provider, output_provider)

    @classmethod
    def register_game(cls, game_type: str, game_class: Type[Game]):
        """
        Register a new game type with the factory.

        Args:
            game_type: The key for this game type
            game_class: The Game subclass to register
        """
        cls._games_registry[game_type] = game_class