from fastapi import APIRouter
from app.models import Expense, Transaction
from typing import List

router = APIRouter(prefix="/blackrock/challenge/v1")


def calculate_rounding(amount: float):
    ceiling = ((int(amount) + 99) // 100) * 100
    remanent = ceiling - amount
    return ceiling, remanent


@router.post("/transactions:parse")
def parse_transactions(expenses: List[Expense]):
    results = []

    for exp in expenses:
        ceiling, remanent = calculate_rounding(exp.amount)

        results.append(
            Transaction(
                date=exp.timestamp,
                amount=exp.amount,
                ceiling=ceiling,
                remanent=remanent,
            )
        )

    return results