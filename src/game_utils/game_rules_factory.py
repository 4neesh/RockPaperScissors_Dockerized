from typing import Dict, Type

from src.game_utils.game_rules import GameRules
from src.game_utils.hand_gesture import HandGesture
from src.game_utils.rps_rules import RPSRules
from constants import GameConfig, FactoryConfig


class GameRulesFactory:
    """
    Factory class for creating game rule objects.
    This factory makes it easy to create the appropriate rules implementation for different games.
    """

    # Registry of game rule implementations
    _rules_registry: Dict[str, Type[GameRules]] = {
        GameConfig.GAME_TYPE: RPSRules
    }

    @classmethod
    def create_rules(cls, game_type: str) -> GameRules:
        """
        Creates a rules instance for the specified game type.

        Args:
            game_type: The type of game rules to create (e.g., "rps" for Rock-Paper-Scissors)

        Returns:
            An instance of the appropriate GameRules implementation

        Raises:
            ValueError: If the game type is not supported
        """
        if game_type not in cls._rules_registry:
            raise ValueError(FactoryConfig.UNSUPPORTED_GAME_ERROR.format(game_type=game_type))

        rule_class = cls._rules_registry[game_type]
        return rule_class()

    @classmethod
    def register_rules(cls, game_type: str, rules_class: Type[GameRules]) -> None:
        """
        Register a new rules implementation.

        Args:
            game_type: The type identifier for the game
            rules_class: The class implementing the rules
        """
        cls._rules_registry[game_type] = rules_class 