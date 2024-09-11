import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from src.inferent.ratings import Glicko2, KalmanRating, Rating, BASE_RATING

class TestGlicko2(unittest.TestCase):

    @patch('src.inferent.ratings.Glicko2.Player')
    def test_update_method(self, mock_Player):
        mock_Player.return_value = Glicko2.Player()
        glicko = Glicko2()
        
        # Initialize players
        p1key = 'player1'
        p2key = 'player2'
        outcome = 'win'
        date = datetime(2023, 1, 1)

        # Update ratings
        glicko.update(p1key, p2key, outcome, date)
        
        # Check if players are initialized and updated
        self.assertIn(p1key, glicko.players)
        self.assertIn(p2key, glicko.players)
        self.assertNotEqual(glicko.get_rating(p1key), BASE_RATING)
        self.assertNotEqual(glicko.get_rating(p2key), BASE_RATING)

    def test_g_function(self):
        rd_opp = 30.0
        g_value = Glicko2.g(rd_opp)
        self.assertAlmostEqual(g_value, 0.99549801)

    def test_win_proba(self):
        r = 1500.0
        r_opp = 1600.0
        rd_opp = 30.0
        expected = Glicko2.win_proba(r, r_opp, rd_opp)
        self.assertAlmostEqual(expected, 0.36053226)


class TestKalmanRating(unittest.TestCase):

    def test_update_method(self):
        kalman = KalmanRating(2.50, 1, 0.5, 4, 0.2)
        
        # Initialize players
        p1key = 'player1'
        p2key = 'player2'
        p1ortg = 0.8
        p2ortg = 0.7
        
        # Update ratings
        kalman.update(p1key, p2key, p1ortg, p2ortg)
        
        # Check if ratings are updated
        self.assertIn(p1key, kalman.players)
        self.assertIn(p2key, kalman.players)
        self.assertNotEqual(kalman.get_rating(p1key).o.score, kalman.avg_rtg)
        self.assertNotEqual(kalman.get_rating(p2key).o.score, kalman.avg_rtg)

if __name__ == '__main__':
    unittest.main()
