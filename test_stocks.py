import unittest
from unittest.mock import patch
from datetime import datetime
from stocks import user_input

class test_stocks(unittest.TestCase):
    
    @patch('builtins.input')
    def test_valid_input(self, mock_input):
        mock_input.side_effect = [
            'AAPL', '1', '2', '2025-01-01', '2025-02-01' 
        ]
        result = user_input()
        self.assertEqual(result['symbol'], 'AAPL')
        self.assertEqual(result['chart_type'], 1)
        self.assertEqual(result['time_series_option'], 2)
        self.assertEqual(result['start_date'], datetime(2025, 1, 1))
        self.assertEqual(result['end_date'], datetime(2025, 2, 1))

    @patch('builtins.input')
    def test_invalid_symbol_then_valid(self, mock_input):
        mock_input.side_effect = [
            '', 'AAPL1234', '123', 'msft'
        ] + [
            '1', '2', '2025-01-01', '2025-02-01'
        ]
        result = user_input()
        self.assertEqual(result['symbol'], 'MSFT')

    @patch('builtins.input')
    def test_invalid_chart_type_then_valid(self, mock_input):
        mock_input.side_effect = [
            'AAPL', '5', 'bar', '2', '2', '2025-01-01', '2025-02-01'
        ]
        result = user_input()
        self.assertEqual(result['chart_type'], 2)

    @patch('builtins.input')
    def test_invalid_time_series_then_valid(self, mock_input):
        mock_input.side_effect = [
            'AAPL', '1', '7', 'x', '3', '2025-01-01', '2025-02-01'
        ]
        result = user_input()
        self.assertEqual(result['time_series_option'], 3)

    @patch('builtins.input')
    def test_invalid_dates_then_valid(self, mock_input):
        mock_input.side_effect = [
            'AAPL', '1', '1',
            '2025-02-30', '2025-01-01',
            '2024-12-01', '2025-01-01'
        ]
        result = user_input()
        self.assertEqual(result['start_date'], datetime(2025, 1, 1))
        self.assertEqual(result['end_date'], datetime(2025, 1, 1))

if __name__ == '__main__':
    unittest.main()
