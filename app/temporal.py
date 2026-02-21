from fastapi import APIRouter
from datetime import datetime
from app.models import TemporalRequest

router = APIRouter(prefix="/blackrock/challenge/v1")


def parse_date(d):
    return datetime.strptime(d, "%Y-%m-%d %H:%M:%S")


def in_range(ts, start, end):
    return start <= ts <= end


@router.post("/transactions:filter")
def filter_transactions(req: TemporalRequest):

    valid = []
    invalid = []

    q_periods = [
        (parse_date(q.start), parse_date(q.end), q.fixed)
        for q in req.q
    ]

    p_periods = [
        (parse_date(p.start), parse_date(p.end), p.extra)
        for p in req.p
    ]

    for tx in req.transactions:
        try:
            t = parse_date(tx.date)

            rem = tx.remanent

            # Apply q override
            applicable_q = [
                q for q in q_periods if in_range(t, q[0], q[1])
            ]

            if applicable_q:
                best = max(applicable_q, key=lambda x: x[0])
                rem = best[2]

            # Apply p additions
            for p in p_periods:
                if in_range(t, p[0], p[1]):
                    rem += p[2]

            tx.remanent = rem
            valid.append(tx)

        except Exception as e:
            invalid.append({**tx.dict(), "message": str(e)})

    return {"valid": valid, "invalid": invalid}