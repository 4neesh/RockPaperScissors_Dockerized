from typing import Dict, Type

from game import Game
from src.io_utils.input_provider import InputProvider
from src.io_utils.output_provider import OutputProvider
from constants import FactoryConfig


class GameFactory:
    """
    Factory class for creating game instances.

    This class implements the Factory pattern to create game objects of different types,
    allowing the system to be extended with new games without modifying existing code.
    """

    # Registry of available game implementations
    _game_registry: Dict[str, Type[Game]] = {}

    @classmethod
    def create_game(cls, game_type: str, input_provider: InputProvider,
                    output_provider: OutputProvider) -> Game:
        """
        Creates a game instance of the specified type.

        Args:
            game_type: The type of game to create
            input_provider: The input provider to use for the game
            output_provider: The output provider to use for the game

        Returns:
            An instance of the game

        Raises:
            ValueError: If the game type is not registered
        """
        if game_type not in cls._game_registry:
            raise ValueError(FactoryConfig.UNSUPPORTED_GAME_ERROR.format(game_type=game_type))

        game_class = cls._game_registry[game_type]
        return game_class(input_provider, output_provider)

    @classmethod
    def register_game(cls, game_type: str, game_class: Type[Game]) -> None:
        """
        Register a new game implementation.

        Args:
            game_type: The identifier for the game type
            game_class: The class implementing the game
        """
        cls._game_registry[game_type] = game_class