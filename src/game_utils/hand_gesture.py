import random
from enum import Enum
from src.constants import GameConstants, RPSGameConstants


class HandGesture(Enum):
    """
    Enum class representing different hand gestures used in the game.
    Each gesture is associated with a unique number.
    """

    ROCK = GameConstants.GESTURE_ROCK
    PAPER = GameConstants.GESTURE_PAPER
    SCISSORS = GameConstants.GESTURE_SCISSORS

    @classmethod
    def choices(cls) -> list[str]:
        """
        Returns a list of formatted strings representing available gestures.

        Returns:
            A list of strings in the format "1 = Rock", "2 = Paper", etc.
        """
        return [RPSGameConstants.GESTURE_FORMAT.format(
            value=move.value,
            name=move.name.capitalize()
        ) for move in cls]

    def __str__(self):
        """
        String representation of the gesture.

        Returns:
            The capitalized name of the gesture
        """
        return self.name.capitalize()

    @staticmethod
    def generate_random_gesture() -> "HandGesture":
        """
        Generates a random gesture.

        Returns:
            A random HandGesture enum value
        """
        return random.choice(list(HandGesture))

    @staticmethod
    def get_gesture_by_number(number: int) -> "HandGesture":
        """
        Gets a gesture by its numeric value.

        Args:
            number: The numeric value of the gesture

        Returns:
            The corresponding HandGesture enum value
        """
        return HandGesture(number)

    @staticmethod
    def validate_entry(value: int) -> bool:
        """
        Validates if a number corresponds to a valid gesture.

        Args:
            value: The numeric value to validate

        Returns:
            True if valid, False otherwise
        """
        return value in [gesture.value for gesture in HandGesture]