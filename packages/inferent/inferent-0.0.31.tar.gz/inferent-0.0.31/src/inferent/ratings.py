"""A module for rating systems, e.g. ELO."""

import logging
from math import sqrt, log, pi, isnan
from copy import copy
from datetime import datetime
from typing import Optional, Dict
from dataclasses import dataclass

# Constants
BASE_RATING = 1500.0
BASE_RD = 350.0
Q = log(10.0) / 400.0

# Logging setup
logger = logging.getLogger("ratings")
logger.setLevel(logging.INFO)


@dataclass
class Rating:
    """Represents a mutable rating that changes over time."""
    score: float
    stdev: float

class Glicko2:
    """Implements Glicko-2 rating system for players.

    See http://www.glicko.net/research/gdescrip.pdf for details
    """

    @dataclass
    class Player:
        """Represents a player with a rating and rating deviation."""
        rating: Rating
        last_fight_date: Optional[datetime] = None
        grd: Optional[float] = None  # g(rd), calculated
        win_exp: Optional[float] = None  # Expected win probability, calculated

        def __init__(self, score=BASE_RATING, stdev=BASE_RD):
            self.rating = Rating(BASE_RATING, BASE_RD)


    def __init__(self):
        """Initializes the Glicko2 object with default settings."""
        self.c: float = 0.0
        self.set_c()
        self.players: Dict[str, self.Player] = {}

    def set_c(self, avg_rd: float = 200.0, days: int = 2500) -> None:
        """
        Sets the constant c for rating deviation decay over time.

        Parameters
        ----------
        avg_rd: Average rating deviation.
        days: Number of days over which decay is measured.
        """
        self.c = (BASE_RD**2 - avg_rd**2) / days

    @staticmethod
    def g(rd_opp: float) -> float:
        """
        Calculates the weight for an opponent's rating deviation.

        Parameters
        ----------
        rd_opp: Opponent's rating deviation.

        Returns
        -------
        Weight for opponent's deviation (<=1.0); weights will be higher for
        lower RDs. This is meant to weight opponents with lower RDs more highly
        in the calculation.
        """
        return 1.0 / sqrt(1.0 + (3.0 * Q**2) * (rd_opp**2) / (pi**2))

    @staticmethod
    def win_proba(r: float, r_opp: float, rd_opp: float) -> float:
        """
        Calculates expected win probability against an opponent.

        Parameters
        ----------
        r: Player's rating.
        r_opp: Opponent's rating.
        rd_opp: Opponent's rating deviation.

        Returns
        -------
        Expected win probability.
        """
        return 1.0 / (1.0 + pow(10.0, -Glicko2.g(rd_opp) * (r - r_opp) / 400.0))

    @staticmethod
    def d_squared(grd_opp: float, win_exp: float) -> float:
        """
        Calculates the variance of the rating.

        Parameters
        ----------
        grd_opp: g(rd) value of the opponent
        win_exp: Expected win probability.

        Returns
        -------
        Variance of the rating.
        """
        return (Q**2) * (grd_opp**2) * win_exp * (1.0 - win_exp)

    def update(
        self, p1_key: str, p2_key: str, outcome: str, date: datetime
    ) -> None:
        """
        Updates ratings for two players based on a match outcome.

        Parameters
        ----------
        p1_key: Key for player 1.
        p2_key: Key for player 2.
        outcome: Match outcome ('win', 'loss', or 'draw').
        date: Date of the match.
        """
        outcome_value = (
            0.0 if outcome == "loss" else 1.0 if outcome == "win" else 0.5
        )
        p1 = self.get_or_create_player(p1_key, date)
        p2 = self.get_or_create_player(p2_key, date)

        logger.info("Calculaging updates for %s, %s, %s, %s",
                     p1, p2, outcome_value, date)
        self.calculate_updates(p1, p2, outcome_value, date)

    def get_or_create_player(self, pkey: str, date: datetime) -> Player:
        """
        Gets or creates a player and updates their rating deviation.

        Parameters
        ----------
        pkey: Key for the player.
        date: Date to update the rating deviation.

        Returns
        -------
        The player object.
        """
        if pkey not in self.players:
            self.players[pkey] = self.Player()
        player = self.players[pkey]
        if player.last_fight_date:
            t = (date - player.last_fight_date).days
            player.rating.stdev = min(
                BASE_RD, sqrt(player.rating.stdev**2 + self.c * t)
            )
        player.last_fight_date = date
        return player

    def calculate_updates(
        self,
        p1: Player,
        p2: Player,
        outcome: float,
        date: datetime,
    ) -> None:
        """
        Calculates and applies updates to player ratings.

        Parameters
        ----------
        p1: Player 1 object.
        p2: Player 2 object.
        outcome: Outcome of the match for player 1.
        date: Date of the match.
        """
        p1.grd = Glicko2.g(p1.rating.stdev)
        p1.win_exp = Glicko2.win_proba(
            p1.rating.score, p2.rating.score, p2.rating.stdev
        )
        p2.grd = Glicko2.g(p2.rating.stdev)
        p2.win_exp = Glicko2.win_proba(
            p2.rating.score, p1.rating.score, p1.rating.stdev
        )

        logger.info("winexp: %s, %s", p1.win_exp, p2.win_exp)
        logger.info("Before %s, %s, %s, %s", p1.rating.score, p1.rating.stdev,
                     p2.rating.score, p2.rating.stdev)
        for player_a, player_b, outcome_a in (
            (p1, p2, outcome),
            (p2, p1, 1.0 - outcome),
        ):
            rd2_d2opp = 1.0 / (player_a.rating.stdev**2) + Glicko2.d_squared(
                player_b.grd, player_b.win_exp
            )
            player_a.rating.score += (
                (Q / rd2_d2opp) * player_b.grd * (outcome_a - player_a.win_exp)
            )
            player_a.rating.stdev = sqrt(1.0 / rd2_d2opp)
            player_a.last_fight_date = date
        logger.info("After %s, %s, %s, %s", p1.rating.score, p1.rating.stdev,
                     p2.rating.score, p2.rating.stdev)

    def get_rating(self, pkey: str) -> float:
        """Returns the rating of a player."""
        return self.players.get(pkey, self.Player()).rating.score

    def get_consistent_rating(self, pkey: str) -> float:
        """Returns the conservative rating of a player (rating - rd)."""
        player = self.players.get(pkey, self.Player())
        return player.rating.score - player.rating.stdev

    def get_player_data(self, pkey: str) -> Player:
        """Returns the player data for a given player key."""
        return self.players.get(pkey, self.Player())


class KalmanRating:
    """Implements Kalman Filter based rating system."""

    @dataclass
    class DualRating:
        """Container for offensive and defensive ratings."""

        def __init__(self, rtg: float, var_rtg: float):
            """
            Initializes DualRating with offensive and defensive ratings.

            :param rtg: Initial rating value.
            :param var_rtg: Initial variance of the rating.
            """
            self.o: Rating = Rating(rtg, var_rtg)
            self.d: Rating = Rating(rtg, var_rtg)

    def __init__(
        self,
        avg_rtg: float,
        avg_var_rtg: float,
        var_proc: float,
        var_meas: float,
        min_threshold: float = 0,
    ):
        """
        Initializes the KalmanRating system with given parameters.

        :param avg_rtg: Average rating.
        :param avg_var_rtg: Average variance of the rating.
        :param var_proc: Process variance.
        :param var_meas: Measurement variance.
        :param min_threshold: Minimum threshold for updates.
        """
        self.avg_rtg: float = avg_rtg
        self.avg_var_rtg: float = avg_var_rtg * avg_rtg
        self.var_proc: float = var_proc * avg_rtg
        self.var_meas: float = var_meas * avg_rtg
        self.min_threshold: float = min_threshold
        self.players: Dict[str, KalmanRating.DualRating] = {}

    def update(
        self,
        p1_key: str,
        p2_key: str,
        p1_ortg: float,
        p2_ortg: float,
    ) -> None:
        """
        Updates ratings for two players based on observed ratings.

        :param p1_key: Key for player 1.
        :param p2_key: Key for player 2.
        :param p1_ortg: Observed offensive rating for player 1.
        :param p2_ortg: Observed offensive rating for player 2.
        """
        p1 = self.players.setdefault(
            p1_key, self.DualRating(self.avg_rtg, self.avg_var_rtg)
        )
        p2 = self.players.setdefault(
            p2_key, self.DualRating(self.avg_rtg, self.avg_var_rtg)
        )

        to_update = []
        if not isnan(p1_ortg):
            to_update += [
                (p1.o, copy(p2.d), p1_ortg),
                (p2.d, copy(p1.o), p1_ortg),
            ]
        if not isnan(p2_ortg):
            to_update += [
                (p2.o, copy(p1.d), p2_ortg),
                (p1.d, copy(p2.o), p2_ortg),
            ]

        for rating1, rating2, observed_rating in to_update:
            self.update_rating(rating1, rating2, observed_rating)

    def update_rating(
        self,
        rating1: Rating,
        rating2: Rating,
        observed_rating: float,
    ) -> None:
        """
        Updates a player's rating using the Kalman filter equations.

        :param rating1: Rating object to be updated.
        :param rating2: Rating object used for prediction.
        :param observed_rating: Observed rating value.
        """
        predicted_rating = rating1.score + rating2.score - self.avg_rtg
        # predicted_rating = (rating1.score * rating2.score / self.avg_rtg)
        predicted_var = rating1.stdev + self.var_proc
        kalman_gain = predicted_var / (predicted_var + self.var_meas)

        rating1.score += kalman_gain * (observed_rating - predicted_rating)
        rating1.stdev = (1 - kalman_gain) * predicted_var

    def get_rating(self, pkey: str) -> DualRating:
        """Returns the DualRating object for a player."""
        return self.players.get(
            pkey, self.DualRating(self.avg_rtg, self.avg_var_rtg)
        )
