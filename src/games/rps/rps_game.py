"""
Refactored Rock-Paper-Scissors game implementation.

This module provides a cleaner, more modular implementation of the RPS game
that separates concerns and makes it easier to extend to other game types.
"""

import sys
from typing import List

from game import Game
from src.core.game_flow_manager import GameFlowManager
from src.games.rps.rps_constants import RPSConstants, RPSGameConfig
from src.games.rps.rps_rules import RPSRules
from src.game_utils.game_mode import GameMode
from src.game_utils.score_manager_factory import ScoreManagerFactory
from src.io_utils.input_provider import InputProvider
from src.io_utils.output_provider import OutputProvider
from src.players.player import Player
from src.constants import GameConstants, GameMessages


class RPSGame(Game):
    """
    Refactored Rock-Paper-Scissors game implementation.

    This class focuses on high-level game coordination, delegating
    specific responsibilities to specialized components.
    """

    # Game configuration
    GAME_TYPE = RPSConstants.GAME_TYPE
    MAX_ROUNDS = RPSGameConfig.DEFAULT_MAX_ROUNDS
    SCORE_MANAGER_TYPE = RPSGameConfig.SCORE_MANAGER_TYPE

    def __init__(self, input_prov: InputProvider, output_prov: OutputProvider):
        super().__init__(input_prov, output_prov)
        self.rules = RPSRules()
        self.game_flow_manager = GameFlowManager(self.rules, output_prov)

    def start_game(self):
        """Start the RPS game."""
        self.output_provider.introduce_game(RPSConstants.GAME_NAME)
        game_mode = self._select_game_mode()
        players = game_mode.initialise_players_in_game(self)
        self._play_game_sessions(players)

    def _play_game_sessions(self, players: List[Player]):
        """
        Play multiple game sessions with replay capability.

        Args:
            players: List of two players
        """
        replay = GameMessages.REPLAY_YES

        while replay.lower() == GameMessages.REPLAY_YES:
            # Create fresh score manager for each session
            score_manager = ScoreManagerFactory.create_score_manager(
                self.SCORE_MANAGER_TYPE,
                self,
                players[0].get_name(),
                players[1].get_name()
            )

            # Play a single game session
            self._play_single_session(players[0], players[1], score_manager)

            # Show final results and ask for replay
            score_manager.return_game_result()
            replay = self.input_provider.play_again_request()

        self.exit_game()

    def _play_single_session(self, player_1: Player, player_2: Player, score_manager):
        """
        Play a single game session.

        Args:
            player_1: The first player
            player_2: The second player
            score_manager: Score manager for this session
        """
        game_option = self._request_game_option()

        if game_option == GameConstants.BEST_OF_5_COMMAND:
            # Best of 5 mode
            self.game_flow_manager.play_best_of_series(
                player_1, player_2, score_manager
            )
        else:
            # Standard rounds mode
            rounds_to_play = int(game_option)
            self.game_flow_manager.play_standard_rounds(
                rounds_to_play, player_1, player_2, score_manager
            )

    def _request_game_option(self) -> str:
        """
        Request the game option from the user.

        Returns:
            Either a number of rounds or "bo5" for best of 5
        """
        prompt = GameMessages.ROUNDS_PROMPT.format(
            min=GameConstants.MIN_ROUNDS,
            max=self.MAX_ROUNDS,
            bo5=GameConstants.BEST_OF_5_COMMAND
        )

        game_option = input(prompt).strip().lower()

        # Validate input
        while not self._is_valid_game_option(game_option):
            game_option = input(prompt).strip().lower()

        return game_option

    def _is_valid_game_option(self, option: str) -> bool:
        """
        Validate the game option input.

        Args:
            option: The user's input

        Returns:
            True if valid, False otherwise
        """
        # Check for best of 5 option
        if option == GameConstants.BEST_OF_5_COMMAND:
            return True

        # Check for valid rounds number
        if option.isdigit():
            rounds = int(option)
            if GameConstants.MIN_ROUNDS <= rounds <= self.MAX_ROUNDS:
                return True

        # Invalid input
        self.output_provider.output_rounds_error(self.MAX_ROUNDS)
        return False

    def _select_game_mode(self) -> GameMode:
        """
        Select the game mode (player configuration).

        Returns:
            The selected GameMode
        """
        while True:
            game_mode_input = self.input_provider.game_mode_request()

            if game_mode_input.isdigit():
                game_mode_number = int(game_mode_input)
                if 1 <= game_mode_number <= len(GameMode):
                    return GameMode.get_game_mode_by_number(game_mode_number)

            self.output_provider.output_game_mode_error()

    def exit_game(self):
        """Exit the game."""
        self.output_provider.output_end_game()
        sys.exit(0)