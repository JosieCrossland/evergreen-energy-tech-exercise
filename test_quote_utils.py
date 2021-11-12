import unittest
from parameterized import parameterized
import quote_utils as sut


class TestQuoteUtils(unittest.TestCase):
    def setUp(self) -> None:
        self.heat_pump_test_data = [
            {
                "label": "5kW package",
                "outputCapacity": 5,
                "costs": [
                    {"label": "Design", "cost": 2000},
                    {"label": "Installation", "cost": 1500},
                    {"label": "Cups of tea", "cost": 20},
                ],
            },
            {
                "label": "2kW package",
                "outputCapacity": 2,
                "costs": [
                    {"label": "Design", "cost": 4000},
                    {"label": "Installation", "cost": 1500},
                    {"label": "Cups of tea", "cost": 40},
                ],
            },
            {
                "label": "10kW package",
                "outputCapacity": 10,
                "costs": [
                    {"label": "Design", "cost": 6000},
                    {"label": "Installation", "cost": 1500},
                    {"label": "Cups of tea", "cost": 900},
                ],
            },
        ]

    def test_calculate_heat_loss(self):
        floor_area = 125
        heating_factor = 101
        insulation_factor = 1.3
        expected = 16412.5
        actual = sut.calculate_heat_loss(floor_area, heating_factor, insulation_factor)
        self.assertEqual(expected, actual)

    def test_calculate_power_heat_loss(self):
        heat_loss = 16412.5
        heating_degree_days = 2483
        expected = 6.6
        actual = sut.calculate_power_heat_loss(heat_loss, heating_degree_days)
        self.assertEqual(expected, actual)

    @parameterized.expand(
        [
            (2, "2kW package"),
            (2.1, "5kW package"),
            (5.1, "10kW package"),
            (11, "required capacity exceeds current heat pump range"),
        ]
    )
    def test_select_heat_pump(self, required_capacity, expected):
        actual = sut.select_heat_pump(self.heat_pump_test_data, required_capacity)
        self.assertEqual(expected, actual.get("label"))

    @parameterized.expand(
        [
            (0, 3696.00),
            (1, 5817.00),
            (2, 8820.00),
        ]
    )
    def test_calculate_total_installation_cost(self, pump_index, expected):
        selected_heat_pump = self.heat_pump_test_data[pump_index]
        vat_rate = 5
        actual = sut.calculate_total_installation_cost(selected_heat_pump, vat_rate)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
