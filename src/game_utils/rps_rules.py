from typing import Dict, List

from src.game_utils.game_rules import GameRules
from src.game_utils.hand_gesture import HandGesture
from constants import Messages, ScoringConfig


class RPSRules(GameRules[HandGesture]):
    """
    Implementation of Rock-Paper-Scissors game rules.
    """

    # Each gesture maps to a list of gestures it beats
    _rules: Dict[HandGesture, List[HandGesture]] = {
        HandGesture.ROCK: [HandGesture.SCISSORS],
        HandGesture.PAPER: [HandGesture.ROCK],
        HandGesture.SCISSORS: [HandGesture.PAPER],
    }

    # Descriptions for each gesture interaction
    _descriptions: Dict[HandGesture, Dict[HandGesture, str]] = {
        HandGesture.ROCK: {HandGesture.SCISSORS: Messages.ROCK_BLUNTS_SCISSORS},
        HandGesture.PAPER: {HandGesture.ROCK: Messages.PAPER_WRAPS_ROCK},
        HandGesture.SCISSORS: {HandGesture.PAPER: Messages.SCISSORS_CUTS_PAPER},
    }

    def determine_result(self, move_1: HandGesture, move_2: HandGesture) -> int:
        """
        Determine the result of a comparison between two moves.

        Args:
            move_1: The first player's gesture
            move_2: The second player's gesture

        Returns:
            1 if move_1 wins, -1 if move_2 wins, 0 if draw
        """
        if move_1 == move_2:
            return ScoringConfig.DRAW_RESULT
        elif move_2 in self._rules.get(move_1, []):
            return ScoringConfig.PLAYER_1_WIN
        elif move_1 in self._rules.get(move_2, []):
            return ScoringConfig.PLAYER_2_WIN
        else:
            raise ValueError(f"No rule defined between {move_1} and {move_2}")

    def get_interaction_description(self, move_1: HandGesture, move_2: HandGesture) -> str:
        """
        Get a description of the interaction between two gestures.

        Args:
            move_1: The first player's gesture
            move_2: The second player's gesture

        Returns:
            A string describing the interaction
        """
        if move_1 == move_2:
            return Messages.DRAW_DESCRIPTION_FORMAT.format(move1=move_1, move2=move_2)
        if move_2 in self._descriptions.get(move_1, {}):
            action = self._descriptions[move_1][move_2]
            return Messages.INTERACTION_FORMAT.format(winner_move=move_1, action=action, loser_move=move_2)
        if move_1 in self._descriptions.get(move_2, {}):
            action = self._descriptions[move_2][move_1]
            return Messages.INTERACTION_FORMAT.format(winner_move=move_2, action=action, loser_move=move_1)
        return Messages.NO_DESCRIPTION_FORMAT.format(move1=move_1, move2=move_2)

    def get_valid_moves(self) -> list[HandGesture]:
        """
        Get the list of valid moves for the game.

        Returns:
            List of all valid HandGesture values
        """
        return list(HandGesture) 