import random
from enum import Enum
from constants import HandGestureConfig, Messages


class HandGesture(Enum):
    """
    Enum class representing different hand gestures used in the game.
    Each gesture is associated with a unique number.
    """

    ROCK = HandGestureConfig.ROCK_VALUE
    PAPER = HandGestureConfig.PAPER_VALUE
    SCISSORS = HandGestureConfig.SCISSORS_VALUE

    @classmethod
    def choices(cls) -> list[str]:
        """
        Returns a list of formatted strings representing available gestures.

        Returns:
            A list of strings in the format "1 = Rock", "2 = Paper", etc.
        """
        return [Messages.GESTURE_CHOICE_FORMAT.format(
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