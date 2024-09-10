from __future__ import annotations
from enum import Enum
from datetime import datetime
from typing import List, Optional, Dict,Any
from pydantic import BaseModel
from dataclasses import dataclass

class OrderStatus(Enum): #TODO: #1 Not yet implemented. 
    LOCAL = "LOCAL"
    UNCONFIRMED = "UNCONFIRMED"
    CONFIRMED = "CONFIRMED"
    NEW = "NEW"
    CANCELLING = "CANCELLING"
    CANCELLED = "CANCELLED"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    REJECTED = "REJECTED"
    REPLACING = "REPLACING"
    REPLACED = "REPLACED"


class TransactionType(Enum):
    WITHDRAW = "WITHDRAW" 
    DEPOSIT = "DEPOSIT" 
    FEE = "FEE"
    TRANSFER = "TRANSFER"

'''
Account Data Classes
'''
class AccountMetadata(BaseModel):
    id:Optional[int]
    currencyCode:Optional[str]

class AccountCash(BaseModel):
    free:float
    total:float
    ppl:float
    result:float
    invested:float
    pieCash:float
    blocked:float | None

'''
Personal Portfolio Classes
'''
class Position(BaseModel):
    ticker: str
    quantity: float
    averagePrice: float
    currentPrice: float
    ppl: float
    fxPpl: float
    initialFillDate: str
    frontend: str
    maxBuy: float
    maxSell: float
    pieQuantity: float

# class Positions(BaseModel):
#     positions: List[Position]

'''
Instruments Metadata CLasses
'''
class TimeEvent(BaseModel):
    date: str
    type: str

class WorkingSchedule(BaseModel):
    id: int
    timeEvents: List[TimeEvent]

class Exchange(BaseModel):
    id: int
    name: str
    workingSchedules: Optional[List[WorkingSchedule]]

class Exchanges(BaseModel):
    exchanges: List[Exchange]


class Instrument(BaseModel):
    addedOn: str
    currencyCode:str
    isin:str
    maxOpenQuantity: int | float
    minTradeQuantity: int | float
    name:str
    shortname: Optional[str]
    ticker: str
    type: str
    workingScheduleId:int

class Instruments(BaseModel):
    instruments: List[Instrument]

'''
Pie Classes Section
'''
# Pie
class dividendCashAction(Enum):
    REINVESTED = "REINVESTED"
    TO_ACCOUNT_CASH = "TO_ACCOUNT_CASH"

class Icon(Enum):
    HOME = "Home"
    PIGGY_BANK = "PiggyBank"
    ICEBERG = "Iceberg"
    AIRPLANE = "Airplane"
    RV = "RV"
    UNICORN = "Unicorn"
    WHALE = "Whale"
    CONVERTIBLE = "Convertible"
    FAMILY = "Family"
    COINS = "Coins"
    EDUCATION = "Education"
    BILLS_AND_COINS = "BillsAndCoins"
    BILLS = "Bills"
    WATER = "Water"
    WIND = "Wind"
    CAR = "Car"
    BRIEFCASE = "Briefcase"
    MEDICAL = "Medical"
    LANDSCAPE = "Landscape"
    CHILD = "Child"
    VAULT = "Vault"
    TRAVEL = "Travel"
    CABIN = "Cabin"
    APARTMENTS = "Apartments"
    BURGER = "Burger"
    BUS = "Bus"
    ENERGY = "Energy"
    FACTORY = "Factory"
    GLOBAL = "Global"
    LEAF = "Leaf"
    MATERIALS = "Materials"
    PILL = "Pill"
    RING = "Ring"
    SHIPPING = "Shipping"
    STOREFRONT = "Storefront"
    TECH = "Tech"
    UMBRELLA = "Umbrella"
    NONE = ''

class PieIssueName(Enum):
    DELISTED = "DELISTED"
    SUSPENDED = "SUSPENDED"
    NO_LONGER_TRADABLE = "NO_LONGER_TRADABLE"
    MAX_POSITION_SIZE_REACHED = "MAX_POSITION_SIZE_REACHED"
    APPROACHING_MAX_POSITION_SIZE = "APPROACHING_MAX_POSITION_SIZE"
    COMPLEX_INSTRUMENT_APP_TEST_REQUIRED = "COMPLEX_INSTRUMENT_APP_TEST_REQUIRED"
    NONE = ''

class PieIssueTransactionType(Enum):
    IRREVERSIBLE = "IRREVERSIBLE"
    REVERSIBLE = "REVERSIBLE"
    INFORMATIVE = "INFORMATIVE"

class PieIssue(BaseModel):
    name: Optional[PieIssueName] = None
    severity: Optional[PieIssueTransactionType] = None

class Result(BaseModel):
    investedValue: Optional[float]= None
    result: Optional[float] = None
    resultCoef: Optional[float] = None
    value: Optional[float] = None

class PieInstrument(BaseModel):
    currentShare: Optional[float] = None
    expectedShare: Optional[float] = None
    issues: Optional[List[PieIssue]] = None
    ownedQuantity: Optional[float] = None
    result: Optional[Result] = None
    ticker: str = None

class PieSettings(BaseModel):
    creationDate: Optional[str] = None
    dividendCashAction: Optional[str] = None
    endDate: Optional[str] = None
    goal: Optional[float] = None
    icon: Optional[Icon] = None
    id: Optional[int] = None
    initialInvestment: Optional[float] = None
    instrumentShares: Optional[Dict[str, float]] = None
    name: Optional[str] = None
    pubicUrl:Optional[str] = None

class Pie(BaseModel):
    instruments: Optional[List[PieInstrument]] = None
    settings: Optional[PieSettings] = None

# Create pie
class CreatePie(BaseModel):
    dividendCashAction: str
    endDate: str
    goal: float
    icon: str
    instrumentShares: Dict[str, float]
    name: str

# Pie List
class PieStatus(Enum):
    """Status of the pie based on the set goal"""
    AHEAD = "AHEAD"
    ON_TRACK = "ON_TRACK"
    BEHIND = "BEHIND"

class DividendDetails(BaseModel):
    gained:Optional[float]
    inCash:Optional[float]
    reinvested:Optional[float]

class PieListItem(BaseModel):
    cash:Optional[float] # Amount of money put into the pie in account currency
    dividendDetails:DividendDetails
    id:Optional[int]
    progress:Optional[float] # Progress of the pie based on the set goal
    result:Optional[Result]
    status:Optional[PieStatus]

class PieList(BaseModel):
    pies:List[PieListItem]

'''
Equity Orders Classes
'''
class Order(BaseModel):
    creationTime: Optional[str] = None
    filledQuantity: Optional[float] = None
    filledValue: Optional[float] = None
    id: Optional[int] = None
    status: Optional[OrderStatus] = None
    strategy: Optional[str] = None
    type: Optional[str] = None
    value: Optional[float] = None
    # New Order Parameters
    limitPrice: Optional[float] = None
    quantity: Optional[float] = None
    ticker: Optional[str] = None
    timeValidity: Optional[str] = None
    stopPrice: Optional[str] = None

class Orders(BaseModel):
    orders: List[Order]

'''
Historical Items Classes
'''
class Tax(BaseModel):
    fillId: Optional[str]
    name: Optional[str]
    quantity: Optional[float]
    timeCharged: Optional[datetime]

class HistoricalOrder(BaseModel):
    dateCreated: Optional[datetime]
    dateExecuted: Optional[datetime]
    dateModified: Optional[datetime]
    executor: Optional[str]
    fillCost: Optional[float]
    fillId: Optional[int]
    fillPrice: Optional[float]
    fillResult: Optional[float]
    fillType: Optional[str]
    filledQuantity: Optional[float]
    filledValue: Optional[float]
    id: Optional[int]
    limitPrice: Optional[float]
    orderedQuantity: Optional[float]
    orderedValue: Optional[float]
    parentOrder: Optional[int]
    status: Optional[str]
    stopPrice: Optional[int]
    taxes: Optional[List[Tax]]
    ticker: Optional[str]
    timeValidity: Optional[str]
    type: Optional[str]

class HistoricalOrderResponseModel(BaseModel):
    items: Optional[List[HistoricalOrder]]
    nextPagePath: Optional[str] = None

class HistoricalItem(BaseModel):
    cursor:Optional[int]=None
    ticker:Optional[str]=None
    limit:Optional[int]=None

# Dividend
class DividendItem(BaseModel):
    amount: Optional[float]
    amountInEuro: Optional[float]
    grossAmountPerShare: Optional[float]
    paidOn: Optional[datetime]
    quantity: Optional[float]
    reference: Optional[str]
    ticker: Optional[str]
    type: Optional[str]

class DividendResponseModel(BaseModel):
    items: Optional[List[DividendItem]]
    nextPagePath: Optional[str]

# Export List
class DataIncluded(BaseModel):
    includeDividends: bool
    includeInterest: bool
    includeOrders: bool
    includeTransactions: bool

class ExportReport(BaseModel):
    dataIncluded: Optional[DataIncluded]
    downloadLink: Optional[str]
    reportId: Optional[int]
    status: Optional[str]
    timeFrom: Optional[datetime]
    timeTo: Optional[datetime]
    response: Optional[str]

# Exports
class DataIncluded(BaseModel):
    includeDividends: bool
    includeInterest: bool
    includeOrders: bool
    includeTransactions: bool

class ExportPayload(BaseModel):
    dataIncluded: DataIncluded
    timeFrom: datetime
    timeTo: datetime

class ExportReportResponse(BaseModel):
    reportId: Optional[int]

# Transaction List
class TransactionPayload(BaseModel):
    cursor: str
    limit: int = 20

class TransactionItem(BaseModel):
    amount: Optional[float]
    dateTime: Optional[datetime]
    reference: Optional[str]
    type: Optional[TransactionType]

class Transactions(BaseModel):
    items: Optional[List[TransactionItem]]
    nextPagePath: Optional[str]