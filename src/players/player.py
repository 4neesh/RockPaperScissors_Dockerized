from abc import abstractmethod, ABC
from constants import GameConfig, ValidationConfig


class Player(ABC):
    """
    Abstract base class representing a player in the Paper, Scissors, Rock game.
    This class serves as a template for both human and computer players, providing
    common functionality like player name and move validation.
    """
    MAX_NAME_LENGTH = GameConfig.MAX_NAME_LENGTH
    DEFAULT_TIME_LIMIT = GameConfig.DEFAULT_TIME_LIMIT

    def __init__(self, name: str, time_limit: int = DEFAULT_TIME_LIMIT):
        self.name = name
        self.time_limit = time_limit

    def get_name(self):
        return self.name

    @abstractmethod
    def make_move(self):
        pass

    @staticmethod
    def name_is_invalid(name: str) -> bool:
        return len(name) == ValidationConfig.EMPTY_STRING_LENGTH or len(name) > Player.MAX_NAME_LENGTH