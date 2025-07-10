from typing import Type, Dict

from src.game_utils.game_rules import GameRules
from src.game_utils.rps_rules import RPSRules
from src.constants import GameConstants, GameMessages


class GameRulesFactory:
    """
    Factory class for creating game rules instances.

    This factory supports creating different rule sets for various games.
    """

    _rules_registry: Dict[str, Type[GameRules]] = {
        GameConstants.GAME_TYPE_RPS: RPSRules
    }

    @classmethod
    def create_rules(cls, game_type: str) -> GameRules:
        """
        Create a game rules instance based on the game type.

        Args:
            game_type: The type of game rules to create (e.g., "rps" for Rock-Paper-Scissors)

        Returns:
            An instance of the appropriate GameRules subclass

        Raises:
            ValueError: If the game type is not supported
        """
        if game_type not in cls._rules_registry:
            raise ValueError(GameMessages.UNSUPPORTED_GAME_TYPE.format(game_type=game_type))

        rules_class = cls._rules_registry[game_type]
        return rules_class()

    @classmethod
    def register_rules(cls, game_type: str, rules_class: Type[GameRules]):
        """
        Register a new game rules type with the factory.

        Args:
            game_type: The key for this rules type
            rules_class: The GameRules subclass to register
        """
        cls._rules_registry[game_type] = rules_class