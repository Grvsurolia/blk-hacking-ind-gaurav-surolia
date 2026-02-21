from fastapi import APIRouter
from datetime import datetime
from app.models import ReturnsRequest
import math

router = APIRouter(prefix="/blackrock/challenge/v1")


def parse_date(d):
    return datetime.strptime(d, "%Y-%m-%d %H:%M:%S")


def tax(income: float):
    if income <= 700000:
        return 0
    elif income <= 1000000:
        return (income - 700000) * 0.10
    elif income <= 1200000:
        return 30000 + (income - 1000000) * 0.15
    elif income <= 1500000:
        return 60000 + (income - 1200000) * 0.20
    else:
        return 120000 + (income - 1500000) * 0.30


def compute_returns(amount, rate, years, inflation):
    final = amount * ((1 + rate) ** years)
    real = final / ((1 + inflation) ** years)
    profit = real - amount
    return real, profit


def apply_temporal_rules(tx, q, p):

    t = parse_date(tx.date)
    rem = tx.remanent

    applicable_q = [
        qx for qx in q if qx[0] <= t <= qx[1]
    ]

    if applicable_q:
        best = max(applicable_q, key=lambda x: x[0])
        rem = best[2]

    for px in p:
        if px[0] <= t <= px[1]:
            rem += px[2]

    return rem


def group_k(transactions, k_periods):

    results = []

    for k in k_periods:
        start, end = k

        total = 0

        for tx in transactions:
            t = parse_date(tx.date)
            if start <= t <= end:
                total += tx.remanent

        results.append((start, end, total))

    return results


@router.post("/returns:nps")
def returns_nps(req: ReturnsRequest):

    years = max(60 - req.age, 5)
    annual_income = req.wage * 12

    q = [(parse_date(x.start), parse_date(x.end), x.fixed) for x in req.q]
    p = [(parse_date(x.start), parse_date(x.end), x.extra) for x in req.p]
    k = [(parse_date(x.start), parse_date(x.end)) for x in req.k]

    for tx in req.transactions:
        tx.remanent = apply_temporal_rules(tx, q, p)

    groups = group_k(req.transactions, k)

    savings = []

    for start, end, amount in groups:

        real, profit = compute_returns(
            amount, 0.0711, years, req.inflation
        )

        deduction = min(amount, 0.10 * annual_income, 200000)

        tax_benefit = tax(annual_income) - tax(
            annual_income - deduction
        )

        savings.append(
            {
                "start": start,
                "end": end,
                "amount": amount,
                "profits": profit,
                "taxBenefit": tax_benefit,
            }
        )

    return {"savingsByDates": savings}


@router.post("/returns:index")
def returns_index(req: ReturnsRequest):

    years = max(60 - req.age, 5)

    q = [(parse_date(x.start), parse_date(x.end), x.fixed) for x in req.q]
    p = [(parse_date(x.start), parse_date(x.end), x.extra) for x in req.p]
    k = [(parse_date(x.start), parse_date(x.end)) for x in req.k]

    for tx in req.transactions:
        tx.remanent = apply_temporal_rules(tx, q, p)

    groups = group_k(req.transactions, k)

    savings = []

    for start, end, amount in groups:

        real, profit = compute_returns(
            amount, 0.1449, years, req.inflation
        )

        savings.append(
            {
                "start": start,
                "end": end,
                "amount": amount,
                "profits": profit,
                "taxBenefit": 0,
            }
        )

    return {"savingsByDates": savings}