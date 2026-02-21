from fastapi import APIRouter
from app.models import TransactionValidatorRequest

router = APIRouter(prefix="/blackrock/challenge/v1")


@router.post("/transactions:validator")
def validate_transactions(req: TransactionValidatorRequest):

    seen = set()
    valid = []
    invalid = []

    for tx in req.transactions:

        if tx.date in seen:
            invalid.append({**tx.dict(), "message": "Duplicate timestamp"})
            continue

        seen.add(tx.date)

        if tx.amount < 0 or tx.remanent < 0:
            invalid.append({**tx.dict(), "message": "Negative values"})
            continue

        valid.append(tx)

    return {"valid": valid, "invalid": invalid}