from abc import ABC, abstractmethod
from game import Game
from constants import ScoringConfig, Messages


class ScoreManager(ABC):
    """
    Abstract base class for score managers.

    Score managers are responsible for tracking scores, displaying leaderboards,
    and determining game results. This abstraction allows for different scoring
    strategies to be implemented without modifying the game logic.
    """

    @abstractmethod
    def return_leaderboard(self) -> None:
        """Display the current leaderboard."""
        pass

    @abstractmethod
    def update_scores_for_round(self, round_result: int) -> None:
        """
        Update scores based on the round result.

        Args:
            round_result: 1 if player 1 wins, -1 if player 2 wins, 0 if draw
        """
        pass

    @abstractmethod
    def return_game_result(self) -> None:
        """Display the final game result."""
        pass

    @abstractmethod
    def get_player_score(self, player_name: str) -> float:
        """
        Get the current score for a specific player.

        Args:
            player_name: The name of the player

        Returns:
            The player's current score
        """
        pass


class StandardScoreManager(ScoreManager):
    """
    Standard implementation of ScoreManager that tracks win/loss/draw scores.

    This implementation awards 1 point for a win, 0.5 for a draw, and 0 for a loss.
    """

    def __init__(self, game: Game, player_1_name: str, player_2_name: str):
        self._scores = {
            player_1_name: ScoringConfig.LOSS_POINTS,
            player_2_name: ScoringConfig.LOSS_POINTS
        }
        self._player_1_name = player_1_name
        self._player_2_name = player_2_name
        self._game = game

    def return_leaderboard(self) -> None:
        self._game.output_provider.output_scores_table(self._scores)

    def update_scores_for_round(self, round_result: int) -> None:
        if round_result == ScoringConfig.PLAYER_1_WIN:
            self._scores[self._player_1_name] += ScoringConfig.WIN_POINTS
        elif round_result == ScoringConfig.PLAYER_2_WIN:
            self._scores[self._player_2_name] += ScoringConfig.WIN_POINTS
        else:
            self._scores[self._player_1_name] += ScoringConfig.DRAW_POINTS
            self._scores[self._player_2_name] += ScoringConfig.DRAW_POINTS

    def return_game_result(self) -> None:
        winner = max(self._scores, key=self._scores.get)
        winner_score = self._scores[winner]
        loser = min(self._scores, key=self._scores.get)
        loser_score = self._scores[loser]
        if winner_score == loser_score:
            self._game.output_provider.output_drawn_game()
        else:
            self._game.output_provider.output_game_winner(winner, winner_score, loser_score)

    def get_player_score(self, player_name: str) -> float:
        """Get the current score for a specific player."""
        return self._scores.get(player_name, ScoringConfig.LOSS_POINTS)


class StreakScoreManager(ScoreManager):
    """
    An alternative score manager that tracks winning streaks.

    This implementation rewards consecutive wins with more points:
    - First win: 1 point
    - Second consecutive win: 2 points
    - Third+ consecutive win: 3 points
    - Draw: Resets streak to 0
    - Loss: Resets streak to 0
    """

    def __init__(self, game: Game, player_1_name: str, player_2_name: str):
        self._scores = {
            player_1_name: ScoringConfig.LOSS_POINTS,
            player_2_name: ScoringConfig.LOSS_POINTS
        }
        self._player_1_name = player_1_name
        self._player_2_name = player_2_name
        self._game = game
        self._player_1_streak = ScoringConfig.LOSS_POINTS
        self._player_2_streak = ScoringConfig.LOSS_POINTS

    def return_leaderboard(self) -> None:
        # Create a display that includes streaks
        display_scores = self._scores.copy()
        display_scores[Messages.STREAK_DISPLAY_FORMAT.format(
            player_name=self._player_1_name,
            streak=self._player_1_streak
        )] = display_scores.pop(self._player_1_name)
        display_scores[Messages.STREAK_DISPLAY_FORMAT.format(
            player_name=self._player_2_name,
            streak=self._player_2_streak
        )] = display_scores.pop(self._player_2_name)
        self._game.output_provider.output_scores_table(display_scores)

    def update_scores_for_round(self, round_result: int) -> None:
        if round_result == ScoringConfig.PLAYER_1_WIN:
            # Player 1 wins
            self._player_1_streak += ScoringConfig.PLAYER_1_WIN
            self._player_2_streak = ScoringConfig.LOSS_POINTS
            # Award points based on streak length
            if self._player_1_streak == ScoringConfig.FIRST_WIN_POINTS:
                self._scores[self._player_1_name] += ScoringConfig.FIRST_WIN_POINTS
            elif self._player_1_streak == ScoringConfig.SECOND_WIN_POINTS:
                self._scores[self._player_1_name] += ScoringConfig.SECOND_WIN_POINTS
            else:
                self._scores[self._player_1_name] += ScoringConfig.THIRD_PLUS_WIN_POINTS
        elif round_result == ScoringConfig.PLAYER_2_WIN:
            # Player 2 wins
            self._player_2_streak += ScoringConfig.PLAYER_1_WIN
            self._player_1_streak = ScoringConfig.LOSS_POINTS
            # Award points based on streak length
            if self._player_2_streak == ScoringConfig.FIRST_WIN_POINTS:
                self._scores[self._player_2_name] += ScoringConfig.FIRST_WIN_POINTS
            elif self._player_2_streak == ScoringConfig.SECOND_WIN_POINTS:
                self._scores[self._player_2_name] += ScoringConfig.SECOND_WIN_POINTS
            else:
                self._scores[self._player_2_name] += ScoringConfig.THIRD_PLUS_WIN_POINTS
        else:
            # Draw - reset streaks
            self._player_1_streak = ScoringConfig.LOSS_POINTS
            self._player_2_streak = ScoringConfig.LOSS_POINTS
            # No points awarded for draws

    def return_game_result(self) -> None:
        winner = max(self._scores, key=self._scores.get)
        winner_score = self._scores[winner]
        loser = min(self._scores, key=self._scores.get)
        loser_score = self._scores[loser]
        if winner_score == loser_score:
            self._game.output_provider.output_drawn_game()
        else:
            self._game.output_provider.output_game_winner(winner, winner_score, loser_score)

    def get_player_score(self, player_name: str) -> float:
        """Get the current score for a specific player."""
        return self._scores.get(player_name, ScoringConfig.LOSS_POINTS)