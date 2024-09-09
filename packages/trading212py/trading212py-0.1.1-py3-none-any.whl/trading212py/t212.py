# /bin/bash
import requests
from requests.exceptions import HTTPError
from trading212py.config import API_VERSION,ACCOUNT_TYPE,API_KEY
from typing import Literal, Optional,Dict,Any
from trading212py.base import (Position, AccountMetadata, AccountCash,
                               Exchange, Exchanges, Instrument, Instruments, Pie, PieListItem, PieList,
                               Order, HistoricalItem,HistoricalOrderResponseModel,
                               DividendResponseModel, ExportReport,ExportPayload,ExportReportResponse,
                               Transactions,TransactionPayload,CreatePie)
from functools import wraps
import json
from trading212py.decorators import debug,jsondump,unpacker

class T212:
    def __init__(self) -> None:
        self._base_url: str = f'https://{ACCOUNT_TYPE}.trading212.com/api/{API_VERSION}'
        self._session: requests.Session = requests.Session()
        self._api_key: str | None = self._get_api_key()
    
    def _get_api_key(self) -> str:
        try:
            if API_KEY is None: raise Exception("T212_API_KEY environment variable has been retreived.")
            else: return API_KEY
        except KeyError as e:
            raise Exception(f"{e} - Please set the T212_API_KEY environment variable.")

    def __request(self, method:str=None, endpoint:str=None, query_params=None, json:Optional[Dict]=None, **kwargs) -> requests.Response:
        try:
            response: requests.Response = self._session.request(
                method=method.upper(),
                url=f'{self._base_url}{endpoint}',
                headers={
                    "Authorization": self._api_key,
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                    "content-type": "application/json; charset=UTF-8",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "en-US,en;q=0.9"
                },
                json=json,
                params=query_params, **kwargs
            )
            response.raise_for_status()           
        except HTTPError as http_err:
            print(f'{http_err}')
        except Exception as e:
            if method == 'DELETE':
                if response.status_code == 404:
                    return response.text # Return None or a custom message indicating successful handling of 404
                else: print(f"Error making request: {response.text} - {e}")
            else: print(f"Error making request: {response.text} - {e}")
        else:
            return response.json() if len(response.json())!=0 else None


    # Account Data
    def _get_account_metadata(self):
        return self.__request(method='GET', endpoint='/equity/account/info')
    
    def _get_account_cash(self):
        return self.__request(method='GET', endpoint='/equity/account/cash')
    
    # Personal Portfolio
    def _get_portfolio(self):
        return self.__request(method='GET', endpoint='/equity/portfolio')
    
    def _get_portfolio_ticker(self, ticker):
        return self.__request(method='GET', endpoint=f'/equity/portfolio/{ticker}')

    # Instruments Metadata
    def _get_exchange_list(self):
        return self.__request(method='GET', endpoint='/equity/metadata/exchanges')
    
    def _get_instrument_list(self):
        return self.__request(method='GET', endpoint='/equity/metadata/instruments')
    
    # Pies
    def _get_pie_list(self):
        return self.__request(method='GET', endpoint='/equity/pies')
    
    def _post_create_pie(self, payload):
        return self.__request(method='POST', endpoint='/equity/pies', query_params=payload)
    
    def _delete_delete_pie(self, pie_id):
        return self.__request(method='DELETE', endpoint=f'/equity/pies/{pie_id}')

    def _get_pie(self, pie_id):
        return self.__request(method='GET', endpoint=f'/equity/pies/{pie_id}')
    
    def _post_update_pie(self, pie_id, payload):
        return self.__request(method='POST', endpoint=f'/equity/pies/{pie_id}', query_params=payload)

    # Equity Orders
    def _get_all_orders(self):
        return self.__request(method='GET', endpoint='/equity/orders')
    
    def _post_place_limit_order(self, payload):
        return self.__request(method='POST', endpoint='/equity/orders/limit', query_params=payload)
    
    def _post_place_market_order(self, payload):
        return self.__request(method='POST', endpoint='/equity/orders/market', query_params=payload)
    
    def _post_stop_order(self, payload):
        return self.__request(method='POST', endpoint='/equity/orders/stop', query_params=payload)
                              
    def _post_stop_limit_order(self, payload):
        return self.__request(method='POST', endpoint='/equity/orders/stop_limit', query_params=payload)
    
    def _delete_cancel_order(self, order_id) -> int:
        return self.__request(method='DELETE', endpoint=f'/equity/orders/{order_id}')
    
    def _get_order(self, order_id):
        return self.__request(method='GET', endpoint=f'/equity/orders/{order_id}')
    
    # Historical Items
    def _get_historical_orders(self,payload):
        return self.__request(method='GET', endpoint='/equity/history/orders', query_params=payload)
    
    def _get_dividends(self,payload): #TODO: #2 Dividends function is returning Response code 500 internal server error.
        return self.__request(method='GET', endpoint='/history/dividends', query_params=payload)
    
    def _get_exports_list(self):
        return self.__request(method='GET', endpoint='/history/exports')
    
    def _post_exports(self,payload):
        return self.__request(method='GET', endpoint=f'/history/exports', query_params=payload)
    
    def _get_transactions(self,payload):
        return self.__request(method='GET', endpoint='/history/transactions', query_params=payload)
    

    # Methods
    # Account Data
    @unpacker(cls=AccountMetadata)
    def account_metadata(self):
        '''Returns the account metadata, including account type, currency, and other account details.'''  
        response: requests.Response = self._get_account_metadata()
        return self._get_account_metadata()
    
    @unpacker(cls=AccountCash)
    def account_cash(self) -> list[AccountCash]:
        '''Returns the account cash balance.'''
        return self._get_account_cash()

    # Personal Portfolio
    @unpacker(cls=Position, clsList=True)
    def portfolio(self):
        '''Returns the portfolio, including the positions and metadata for each position.
        '''
        return self._get_portfolio()

    @unpacker(cls=Position)
    def portfolio_ticker(self, ticker) -> Position:
        '''Returns the portfolio details for a specific ticker.

        Args:
            ticker (str): The ticker symbol of the position to retrieve.
        '''
        return self._get_portfolio_ticker(ticker=ticker)

    # Instruments Metadata
    @unpacker(cls=Exchange, clsList=True)
    def exchange_list(self) -> Exchanges:
        '''Returns the list of exchanges supported by Trading212.'''
        return self._get_exchange_list()

    @unpacker(cls=Instrument, clsList=True)
    def instrument_list(self) -> Instruments:
        '''Returns the list of instruments supported by Trading212.'''
        return self._get_instrument_list()

    # Pies
    @unpacker(cls=PieListItem, clsList=True)
    def pie_list(self) -> PieList:
        '''Returns the list of Pies (Portfolio Investment Environments) by the user.
        API Ref: https://t212public-api-docs.redoc.ly/#operation/getAll
        '''
        return self._get_pie_list()

    @unpacker(cls=Pie, clsList=True)
    def create_pie(self, payload:CreatePie) -> Pie:
        '''Creates a new Pie (Portfolio Investment Environment) with the provided payload.
        Ref: https://t212public-api-docs.redoc.ly/#operation/create

        Args:
            payload (dict): The payload containing the details of the new Pie.
        '''
        return self._post_create_pie(payload=payload.model_dump(exclude_none=True))
    
    def delete_pie(self, pie_id:int=None) -> int:
        '''Deletes the Pie with the specified pie_id.

        Args:
            pie_id (str): The ID of the Pie to delete.
        '''
        if not pie_id: raise Exception(f"Provide {pie_id=}")
        else: return self._delete_delete_pie(pie_id=pie_id)

    @unpacker(cls=Pie)
    def pie(self, pie_id:int=None) -> Pie:
        '''Returns the details of the Pie with the specified pie_id.

        Args:
            pie_id (str): The ID of the Pie to retrieve.
        '''
        if not pie_id: raise Exception(f"Provide {pie_id=}")
        else: return self._get_pie(pie_id=pie_id)

    def update_pie(self, pie_id, payload):
        '''Updates the Pie with the specified pie_id using the provided payload.

        Args:
            pie_id (str): The ID of the Pie to update.
            payload (dict): The payload containing the updated details of the Pie.
        '''
        return self._post_update_pie(pie_id=pie_id, payload=payload)

    # Equity Orders
    @unpacker(cls=Order, clsList=True)
    def all_orders(self):
        '''Returns all orders placed by user.'''
        return self._get_all_orders()

    @unpacker(cls=Order)
    def place_limit_order(self, payload:Order):
        '''Places a limit order with the provided payload.

        Args:
            payload (dict): The payload containing the details of the limit order.
        '''
        return self._post_place_limit_order(payload=payload.model_dump(exclude_none=True))

    @unpacker(cls=Order)
    def place_market_order(self, payload:Order):
        '''Places a market order with the provided payload.

        Args:
            payload (dict): The payload containing the details of the market order.
        '''
        return self._post_place_market_order(payload=payload.model_dump(exclude_none=True))

    @unpacker(cls=Order)
    def stop_order(self, payload:Order):
        '''Places a stop order with the provided payload.

        Args:
            payload (dict): The payload containing the details of the stop order.
        '''
        return self._post_stop_order(payload=payload.model_dump(exclude_none=True))

    @unpacker(cls=Order)
    def stop_limit_order(self, payload:Order):
        '''Places a stop limit order with the provided payload.

        Args:
            payload: (dict) The payload containing the details of the stop limit order.
        '''
        return self._post_stop_limit_order(payload=payload.model_dump(exclude_none=True))

    def cancel_order(self, order_id:int=None) -> None:
        '''Cancels the order with the specified order_id.

        Args:
            order_id (str): The ID of the order to cancel.
        '''
        if not order_id: raise Exception(f"Provide {order_id=}")
        else: return self._delete_cancel_order(order_id=order_id)

    @unpacker(cls=Order)
    def order(self, order_id:int=None):
        '''Returns the details of the order with the specified order_id.

        Args:
            order_id (str): The ID of the order to retrieve.
        '''
        return self._get_order(order_id=order_id)

    # Historical Items
    @unpacker(cls=HistoricalOrderResponseModel)
    def historical_orders(self,payload:HistoricalItem):
        '''Returns the historical orders.      
        Args:
            HistoricalItem class
                cursor (int): The cursor value for pagination.
                limit (int): The maximum number of orders to retrieve.
                    Default: 20
                    Max items: 50
                    Example: limit=21
                ticker (str): The ticker symbol to filter orders by.

        Example:
                historicalItem = HistoricalItem(cursor=0,ticker='AAPL_US_EQ',limit=20)
                print(t212.historical_orders(payload=historicalItem))
        '''
        return self._get_historical_orders(payload=payload.model_dump(exclude_none=True))

    
    @unpacker(cls=DividendResponseModel)
    def dividends(self,payload:HistoricalItem):
        '''Returns the dividends.
        Args:
            HistoricalItem class
                cursor (int): The cursor value for pagination.
                limit (int): The maximum number of orders to retrieve.
                    Default: 20
                    Max items: 50
                    Example: limit=21
            ticker (str): The ticker symbol to filter orders by.
        '''
        return self._get_dividends(payload=payload.model_dump(exclude_none=True))

    @unpacker(cls=ExportReport)
    def exports_list(self):
        '''Returns the list of exports.
        NOTE: THIS ENDPOINT IS NOT AVAILABLE FOR IN DEMO MODE.
        '''
        if ACCOUNT_TYPE.upper()=='DEMO': raise Exception(f"This endpoint is not available in {ACCOUNT_TYPE=} mode.")
        else: return self._get_exports_list()

    @unpacker(cls=ExportReportResponse)
    def exports(self, payload:ExportPayload):
        '''Creates a new export with the provided payload.

        Args:
            payload (dict): The payload containing the details of the export.
        
        Example:
            from trading212py.base import ExportPayload
            payload = {
                "dataIncluded": {
                    "includeDividends": True,
                    "includeInterest": True,
                    "includeOrders": True,
                    "includeTransactions": True
                },
                "timeFrom": "2019-08-24T14:15:22Z",
                "timeTo": "2024-09-07T14:15:22Z"
                }
            print(t212.exports(payload=ExportPayload(**payload)))
        '''
        return self._post_exports(payload=payload.model_dump(exclude_none=True))

    @unpacker(cls=Transactions)
    def transactions(self,payload:TransactionPayload):
        '''Returns the transactions.
        
        Args:
            cursor (str) = Pagination cursor
            limit (int) = The maximum number of transactions to retrieve. Default: 20, Max items: 50
        '''
        return self._get_transactions(payload=payload.model_dump(exclude_none=True))