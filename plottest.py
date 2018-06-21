import unittest
from plotter import Plotter


class MyTestCase(unittest.TestCase):
    plotter = Plotter()

    def test_amount_of_goals(self):
        self.assertEqual(self.plotter.get_goals_amount("England"), 2138)
        self.assertEqual(self.plotter.get_goals_amount("Poland"), 1338)

    def test_win_amounts(self):
        self.assertEqual(self.plotter.get_wins("Poland"), 340)
        self.assertEqual(self.plotter.get_wins("Germany"), 545)

    def test_appearances_amount(self):
        self.assertEqual(self.plotter.get_appearances("Poland"), 793)
        self.assertEqual(self.plotter.get_appearances("Italy"), 785)
        self.assertEqual(self.plotter.get_appearances(""), 0)

    def test_take(self):
        x = [i for i in range(10)]
        self.assertEqual(len(Plotter.take(5, x)), 5)
        self.assertNotEqual(len(Plotter.take(0, x)), 5)


if __name__ == '__main__':
    unittest.main()
