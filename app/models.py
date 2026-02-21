from pydantic import BaseModel
from typing import List, Optional


class Expense(BaseModel):
    timestamp: str
    amount: float


class Transaction(BaseModel):
    date: str
    amount: float
    ceiling: float
    remanent: float


class PeriodQ(BaseModel):
    fixed: float
    start: str
    end: str


class PeriodP(BaseModel):
    extra: float
    start: str
    end: str


class PeriodK(BaseModel):
    start: str
    end: str


class TransactionValidatorRequest(BaseModel):
    wage: float
    transactions: List[Transaction]


class TemporalRequest(BaseModel):
    q: List[PeriodQ] = []
    p: List[PeriodP] = []
    k: List[PeriodK] = []
    transactions: List[Transaction]


class ReturnsRequest(BaseModel):
    age: int
    wage: float
    inflation: float
    q: List[PeriodQ] = []
    p: List[PeriodP] = []
    k: List[PeriodK] = []
    transactions: List[Transaction]