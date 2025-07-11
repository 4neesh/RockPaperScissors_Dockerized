"""
Refactored Rock-Paper-Scissors main game entry point.

This file maintains the original interface while using the new
refactored game implementation.
"""

from src.games.rps.rps_game import RPSGame
from src.games.rps.rps_constants import RPSConstants
from src.io_utils.input_provider_console import InputProviderConsole
from src.io_utils.output_provider_console import OutputProviderConsole
from src.game_factory import GameFactory


def main():
    """Main entry point for the Rock-Paper-Scissors game."""
    # Register the game with the factory
    GameFactory.register_game(RPSConstants.GAME_TYPE, RPSGame)

    # Create input/output providers
    input_provider = InputProviderConsole()
    output_provider = OutputProviderConsole()

    # Create the game using the factory
    rps_game = GameFactory.create_game(
        RPSConstants.GAME_TYPE,
        input_provider,
        output_provider
    )

    # Start the game
    rps_game.start_game()


if __name__ == "__main__":
    main()