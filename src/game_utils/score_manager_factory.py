from typing import Type, Dict

from game import Game
from src.game_utils.score_manager import ScoreManager, StandardScoreManager, StreakScoreManager
from src.constants import GameConstants, GameMessages


class ScoreManagerFactory:
    """
    Factory class for creating score manager instances.
    """

    _managers: Dict[str, Type[ScoreManager]] = {
        GameConstants.SCORE_MANAGER_STANDARD: StandardScoreManager,
        GameConstants.SCORE_MANAGER_STREAK: StreakScoreManager
    }

    @classmethod
    def create_score_manager(cls, manager_type: str, game: Game, player_1_name: str,
                             player_2_name: str) -> ScoreManager:
        """
        Create a score manager of the specified type.

        Args:
            manager_type: The type of score manager to create
            game: The game instance
            player_1_name: Name of the first player
            player_2_name: Name of the second player

        Returns:
            An instance of the appropriate ScoreManager subclass

        Raises:
            ValueError: If the manager type is not supported
        """
        if manager_type not in cls._managers:
            raise ValueError(GameMessages.UNSUPPORTED_SCORE_TYPE.format(manager_type=manager_type))

        manager_class = cls._managers[manager_type]
        return manager_class(game, player_1_name, player_2_name)

    @classmethod
    def register_manager(cls, manager_type: str, manager_class: Type[ScoreManager]):
        """
        Register a new score manager type with the factory.

        Args:
            manager_type: The key for this manager type
            manager_class: The ScoreManager subclass to register
        """
        cls._managers[manager_type] = manager_class