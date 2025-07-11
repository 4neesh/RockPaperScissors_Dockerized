from abc import abstractmethod, ABC
from src.constants import PlayerConstants


class Player(ABC):
    """
    Abstract base class representing a player in the game.
    This class serves as a template for both human and computer players, providing
    common functionality like player name and move validation.
    """
    MAX_NAME_LENGTH = PlayerConstants.MAX_NAME_LENGTH
    DEFAULT_TIME_LIMIT = PlayerConstants.DEFAULT_TIME_LIMIT

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
        return (len(name) < PlayerConstants.MIN_NAME_LENGTH or
                len(name) > PlayerConstants.MAX_NAME_LENGTH)
