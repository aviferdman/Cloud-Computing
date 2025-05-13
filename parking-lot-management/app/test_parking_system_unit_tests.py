import unittest
from unittest.mock import patch
from datetime import datetime, timedelta
from parking_system import parked_time_calc, calc_price

class TestParkingSystem(unittest.TestCase):

    @patch('parking_system.datetime')
    def test_parked_time_calc(self, mock_datetime):

        mock_datetime.utcnow.return_value = datetime(2025, 5, 13, 12, 0, 0)
        mock_datetime.fromisoformat.side_effect = datetime.fromisoformat
        entry_time = "2025-05-13T10:00:00"
        expected_parked_time = timedelta(hours=2)

        result = parked_time_calc(entry_time)
        self.assertEqual(result, expected_parked_time)


    @patch('parking_system.parked_time_calc')
    def test_calc_price(self, mock_parked_time_calc):

        mock_parked_time_calc.return_value = timedelta(hours=2)
        entry_time = "2025-05-13T10:00:00"
        expected_charge = 20.0  # 2 hours * $10/hour
        expected_minutes = 120.0

        charge, total_minutes = calc_price(entry_time)
        self.assertEqual(charge, expected_charge)
        self.assertEqual(total_minutes, expected_minutes)

if __name__ == '__main__':
    unittest.main()
