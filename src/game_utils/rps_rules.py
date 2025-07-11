from typing import Dict, List

from src.game_utils.game_rules import GameRules
from src.game_utils.hand_gesture import HandGesture
from src.constants import RPSGameConstants, GameMessages, ScoringConstants


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
        HandGesture.ROCK: {HandGesture.SCISSORS: RPSGameConstants.ROCK_ACTION},
        HandGesture.PAPER: {HandGesture.ROCK: RPSGameConstants.PAPER_ACTION},
        HandGesture.SCISSORS: {HandGesture.PAPER: RPSGameConstants.SCISSORS_ACTION},
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
            return ScoringConstants.DRAW
        elif move_2 in self._rules.get(move_1, []):
            return ScoringConstants.PLAYER_1_WIN
        elif move_1 in self._rules.get(move_2, []):
            return ScoringConstants.PLAYER_2_WIN
        else:
            raise ValueError(GameMessages.NO_RULE_DEFINED.format(
                move1=move_1,
                move2=move_2
            ))

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
            return GameMessages.DRAW_DESCRIPTION.format(move1=move_1, move2=move_2)
        if move_2 in self._descriptions.get(move_1, {}):
            action = self._descriptions[move_1][move_2]
            return GameMessages.WIN_DESCRIPTION.format(
                winner=move_1,
                action=action,
                loser=move_2
            )
        if move_1 in self._descriptions.get(move_2, {}):
            action = self._descriptions[move_2][move_1]
            return GameMessages.WIN_DESCRIPTION.format(
                winner=move_2,
                action=action,
                loser=move_1
            )
        return GameMessages.NO_DESCRIPTION.format(move1=move_1, move2=move_2)

    def get_valid_moves(self) -> list[HandGesture]:
        """
        Get the list of valid moves for the game.

        Returns:
            List of all valid HandGesture values
        """
        return list(HandGesture)