"""
Rock-Paper-Scissors game rules implementation.

This module implements the game rules for RPS using the new move system,
making it easy to extend to other game types.
"""

from typing import Dict, List

from src.game_utils.game_rules import GameRules
from src.games.rps.rps_move import RPSMove
from src.games.rps.rps_constants import RPSConstants
from src.constants import GameMessages, ScoringConstants


class RPSRules(GameRules[RPSMove]):
    """
    Rock-Paper-Scissors rules implementation using the new move system.
    """

    # Define what each move beats
    _victory_rules: Dict[RPSMove, List[RPSMove]] = {
        RPSMove.ROCK: [RPSMove.SCISSORS],
        RPSMove.PAPER: [RPSMove.ROCK],
        RPSMove.SCISSORS: [RPSMove.PAPER],
    }

    # Define interaction descriptions
    _interaction_descriptions: Dict[RPSMove, Dict[RPSMove, str]] = {
        RPSMove.ROCK: {RPSMove.SCISSORS: RPSConstants.ROCK_ACTION},
        RPSMove.PAPER: {RPSMove.ROCK: RPSConstants.PAPER_ACTION},
        RPSMove.SCISSORS: {RPSMove.PAPER: RPSConstants.SCISSORS_ACTION},
    }

    def determine_result(self, move_1: RPSMove, move_2: RPSMove) -> int:
        """
        Determine the result of a comparison between two RPS moves.

        Args:
            move_1: The first player's move
            move_2: The second player's move

        Returns:
            1 if move_1 wins, -1 if move_2 wins, 0 if draw
        """
        if move_1 == move_2:
            return ScoringConstants.DRAW
        elif move_2 in self._victory_rules.get(move_1, []):
            return ScoringConstants.PLAYER_1_WIN
        elif move_1 in self._victory_rules.get(move_2, []):
            return ScoringConstants.PLAYER_2_WIN
        else:
            raise ValueError(GameMessages.NO_RULE_DEFINED.format(
                move1=move_1,
                move2=move_2
            ))

    def get_interaction_description(self, move_1: RPSMove, move_2: RPSMove) -> str:
        """
        Get a description of the interaction between two RPS moves.

        Args:
            move_1: The first player's move
            move_2: The second player's move

        Returns:
            A string describing the interaction
        """
        if move_1 == move_2:
            return GameMessages.DRAW_DESCRIPTION.format(move1=move_1, move2=move_2)

        # Check if move_1 beats move_2
        if move_2 in self._interaction_descriptions.get(move_1, {}):
            action = self._interaction_descriptions[move_1][move_2]
            return GameMessages.WIN_DESCRIPTION.format(
                winner=move_1,
                action=action,
                loser=move_2
            )

        # Check if move_2 beats move_1
        if move_1 in self._interaction_descriptions.get(move_2, {}):
            action = self._interaction_descriptions[move_2][move_1]
            return GameMessages.WIN_DESCRIPTION.format(
                winner=move_2,
                action=action,
                loser=move_1
            )

        return GameMessages.NO_DESCRIPTION.format(move1=move_1, move2=move_2)

    def get_valid_moves(self) -> List[RPSMove]:
        """
        Get all valid RPS moves.

        Returns:
            List of all valid RPSMove values
        """
        return RPSMove.get_all_moves()