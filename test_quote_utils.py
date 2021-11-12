import unittest
from quote_utils import calculate_heat_loss


class TestQuoteUtils(unittest.TestCase):
    def test_calculate_heat_loss(self):
        floor_area = 125
        heating_factor = 101
        insulation_factor = 1.3
        expected = 16412.5
        actual = calculate_heat_loss(floor_area, heating_factor, insulation_factor)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
