import unittest
from backtest_equities import your_main_function


class TestBacktestEquities(unittest.TestCase):

    def test_equity_returns(self):
        # Example test for your backtest logic
        self.assertEqual(your_main_function([100, 110, 105]), 5)  # Example values


if __name__ == '__main__':
    unittest.main()