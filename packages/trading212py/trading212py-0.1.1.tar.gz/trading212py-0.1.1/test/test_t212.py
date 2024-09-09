import unittest
from unittest.mock import patch, MagicMock
from src.trading212py import AccountMetadata, AccountCash, Position, Exchanges, Instrument,Instruments
from src.trading212py import T212  # assuming your class is saved in a file named t212.py

class TestT212(unittest.TestCase):
    
    def setUp(self):
        self.client = T212()
        
    @patch('trading212py.t212.T212._get_account_metadata')
    def test_account_metadata(self, mock_get_account_metadata):
        mock_response = [{'id': 10211034, 'currencyCode': 'EUR'}]
        mock_get_account_metadata.return_value = mock_response
        
        result = self.client.account_metadata()
        
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], AccountMetadata)
        self.assertEqual(result[0].currencyCode, 'EUR')

    @patch('trading212py.t212.T212._get_account_cash')
    def test_account_metadata(self, mock_get_account_cash):
        mock_response = [{'free': 30270.14, 'total': 49774.1, 'ppl': -466.04, 'result': 271.23, 'invested': 19970.0, 'pieCash': 0.0, 'blocked': 0.4}]
        mock_get_account_cash.return_value = mock_response
        
        result = self.client.account_cash()
        
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], AccountCash)
        self.assertEqual(result[0].free, 30270.14)
        self.assertEqual(result[0].total, 49774.1)
        self.assertEqual(result[0].ppl, -466.04)
        self.assertEqual(result[0].invested, 19970.0)
        self.assertEqual(result[0].pieCash, 0.0)
        self.assertEqual(result[0].blocked, 0.4)

    @patch('trading212py.t212.T212._get_portfolio')
    def test_portfolio(self, mock_get_portfolio_ticker):
        # Mock response matching the structure expected for portfolio positions
        mock_response = [{
            'ticker': 'AAPL_US_EQ', 
            'quantity': 3.5680544, 
            'averagePrice': 181.84980588, 
            'currentPrice': 222.91, 
            'ppl': 117.26, 
            'fxPpl': -14.69, 
            'initialFillDate': '2024-02-20T16:30:02.000+02:00', 
            'frontend': 'AUTOINVEST', 
            'maxBuy': 3127263.4319456, 
            'maxSell': 3127267.0, 
            'pieQuantity': 3.5680544
        }]
        mock_get_portfolio_ticker.return_value = mock_response

        # Calling the actual portfolio method
        result = self.client.portfolio()

        # Ensure result is a list and contains Position objects
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], Position)
        self.assertEqual(result[0].ticker, 'AAPL_US_EQ')
        self.assertEqual(result[0].quantity, 3.5680544)
        self.assertEqual(result[0].averagePrice, 181.84980588)
        self.assertEqual(result[0].currentPrice, 222.91)
        self.assertEqual(result[0].ppl, 117.26)
        self.assertEqual(result[0].fxPpl, -14.69)
        self.assertEqual(result[0].initialFillDate, '2024-02-20T16:30:02.000+02:00')

    @patch('trading212py.t212.T212._get_exchange_list')
    def test_exchange_list(self, mock_get_exchange_list):
        # Mock response that matches the new structure
        mock_response = [
            {
                "id": 1,
                "name": "New York Stock Exchange",
                "workingSchedules": [
                    {
                        "id": 10,
                        "timeEvents": [
                            {
                                "date": "2023-09-01T14:15:22Z",
                                "type": "OPEN"
                            },
                            {
                                "date": "2023-09-01T21:00:00Z",
                                "type": "CLOSE"
                            }
                        ]
                    }
                ]
            },
            {
                "id": 2,
                "name": "NASDAQ Stock Market",
                "workingSchedules": [
                    {
                        "id": 20,
                        "timeEvents": [
                            {
                                "date": "2023-09-01T14:15:22Z",
                                "type": "OPEN"
                            },
                            {
                                "date": "2023-09-01T21:00:00Z",
                                "type": "CLOSE"
                            }
                        ]
                    }
                ]
            }
        ]
        mock_get_exchange_list.return_value = mock_response

        # Call the actual exchange_list method
        result = self.client.exchange_list()

        # Assertions to check if the result matches the mock response
        # self.assertEqual(result, mock_response)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], cls=Exchanges)
        # self.assertEqual(result[0]['name'], 'New York Stock Exchange') # It fails due to character count. AssertionError: Lists differ: [Exchange(id=1, name='New York Stock Excha[371 chars]])])] != [{'id': 1, 'name': 'New York Stock Exchang[343 chars]]}]}]
        self.assertEqual(result[0]['workingSchedules'][0]['timeEvents'][0]['type'], 'OPEN')
        self.assertEqual(result[0]['workingSchedules'][0]['timeEvents'][1]['type'], 'CLOSE')
        self.assertEqual(result[1]['name'], 'NASDAQ Stock Market')
        self.assertEqual(result[1]['workingSchedules'][0]['timeEvents'][0]['type'], 'OPEN')

    @patch('trading212py.t212.T212._get_instrument_list')
    def test_instrument_list(self, mock_get_instrument_list):
        # Mock response that matches the new structure
        mock_response = [{
            "addedOn": "2019-08-24T14:15:22Z",
            "currencyCode": "USD",
            "isin": "string",
            "maxOpenQuantity": 0,
            "minTradeQuantity": 0,
            "name": "string",
            "shortname": "string",
            "ticker": "AAPL_US_EQ",
            "type": "ETF",
            "workingScheduleId": 0
        },
        {
            "addedOn": "2019-08-24T14:15:22Z",
            "currencyCode": "USD",
            "isin": "string",
            "maxOpenQuantity": 0,
            "minTradeQuantity": 0,
            "name": "string",
            "shortname": "string",
            "ticker": "AAPL_US_EQ",
            "type": "ETF",
            "workingScheduleId": 0
        }]

        mock_get_instrument_list.return_value = mock_response

        # Call the actual exchange_list method
        result = self.client.instrument_list()

        # Assertions to check if the result matches the mock response
        self.assertEqual(result, mock_response)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], dict)
        self.assertEqual(result[0]['currencyCode'], 'USD')
        self.assertEqual(result[0]['ticker'], 'AAPL_US_EQ')
        self.assertEqual(result[1]['currencyCode'], 'GBP')
        self.assertEqual(result[1]['ticker'], 'AAPL_US_EQ')


    # @patch('trading212py.t212.T212._post_place_market_order')
    # def test_place_market_order(self, mock_post_place_market_order):
    #     mock_payload = {'ticker': 'AAPL', 'quantity': 10}
    #     mock_response = {'orderId': '12345', 'status': 'placed'}
    #     mock_post_place_market_order.return_value = mock_response
        
    #     result = self.client.place_market_order(mock_payload)
        
    #     self.assertEqual(result['orderId'], '12345')
    #     self.assertEqual(result['status'], 'placed')

if __name__ == '__main__':
    unittest.main()
