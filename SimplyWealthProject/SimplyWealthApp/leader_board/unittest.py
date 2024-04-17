import unittest
from unittest.mock import patch
from calculate_weekly_changes import StockPrices

class TestStockPrices(unittest.TestCase):

    @patch('calculate_weekly_changes.requests.get')
    def test_get_current_price(self, mock_get):
        mock_response = {
            'results': [
                {'ticker': 'AAPL', 'price': 150.0},
                {'ticker': 'GOOGL', 'price': 2500.0}
            ]
        }
        mock_get.return_value.json.return_value = mock_response

        current_prices = StockPrices.get_current_price('AAPL')

        expected_prices = {'AAPL': 150.0}
        self.assertEqual(current_prices, expected_prices)

    def test_get_distinct_stocks(self):
        mock_stock_portfolios = [
            {'stock_symbol': 'AAPL'},
            {'stock_symbol': 'GOOGL'}
        ]

        with patch('calculate_weekly_changes.UserStockPortfolio.objects.all') as mock_queryset:
            mock_queryset.return_value = mock_stock_portfolios

            distinct_stocks = StockPrices.get_distinct_stocks()

            expected_stocks = {'AAPL', 'GOOGL'}
            self.assertEqual(distinct_stocks, expected_stocks)

if __name__ == '__main__':
    unittest.main()
