from abc import ABC, abstractmethod

from src.constants import GameConstants
from src.io_utils.input_provider import InputProvider
from src.io_utils.output_provider import OutputProvider


class Game(ABC):
    """
    Abstract base class for games in the arcade system.

    Defines a consistent interface for all game implementations.
    Each game must handle its own startup and shutdown logic, and receive input/output providers for I/O abstraction.
    """

    EXIT_COMMAND = GameConstants.EXIT_COMMAND

    def __init__(self, input_prov: InputProvider, output_prov: OutputProvider):
        super().__init__()
        self.input_provider = input_prov
        self.output_provider = output_prov

    @abstractmethod
    def start_game(self):
        pass

    @abstractmethod
    def exit_game(self):
        pass