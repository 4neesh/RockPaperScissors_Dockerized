from typing import Dict, Type

from game import Game
from src.game_utils.score_manager import ScoreManager, StandardScoreManager, StreakScoreManager


class ScoreManagerFactory:
    """
    Factory class for creating score manager instances.
    
    This factory makes it easy to create the appropriate score manager implementation
    for different scoring strategies and game types.
    """
    
    # Registry of score manager implementations
    _score_manager_registry: Dict[str, Type[ScoreManager]] = {
        "standard": StandardScoreManager,
        "streak": StreakScoreManager
    }
    
    @classmethod
    def create_score_manager(cls, manager_type: str, game: Game, 
                             player_1_name: str, player_2_name: str) -> ScoreManager:
        """
        Creates a score manager instance for the specified type.
        
        Args:
            manager_type: The type of score manager to create
            game: The game instance
            player_1_name: The name of player 1
            player_2_name: The name of player 2
            
        Returns:
            An instance of the appropriate ScoreManager implementation
            
        Raises:
            ValueError: If the manager type is not supported
        """
        if manager_type not in cls._score_manager_registry:
            raise ValueError(f"Unsupported score manager type: {manager_type}")
        
        manager_class = cls._score_manager_registry[manager_type]
        return manager_class(game, player_1_name, player_2_name)
    
    @classmethod
    def register_score_manager(cls, manager_type: str, manager_class: Type[ScoreManager]) -> None:
        """
        Register a new score manager implementation.
        
        Args:
            manager_type: The type identifier for the score manager
            manager_class: The class implementing the score manager
        """
        cls._score_manager_registry[manager_type] = manager_class 