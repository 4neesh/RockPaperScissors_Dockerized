from src.game_utils.hand_gesture import HandGesture
from src.players.player import Player
from game import Game


class ComputerPlayer(Player):
    """
    Represents a computer-controlled player in the game. 
    The computer randomly selects a gesture for its move.
    """
    def __init__(self, game: Game, player_id: int):
        name = f"Computer {player_id}"
        super().__init__(name)
        self._game = game

    def make_move(self) -> HandGesture:
        return HandGesture.generate_random_gesture()