"""
Test Type: Integration + Functional API Testing
Validation:
    - Transaction parsing
    - Transaction validation
    - Temporal filtering
    - Returns calculation (NPS & Index)
    - Performance endpoint
Command:
    pytest -v
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# -------------------------
# Sample Data
# -------------------------

expenses_payload = [
    {
        "timestamp": "2023-10-12 20:15:00",
        "amount": 250
    },
    {
        "timestamp": "2023-02-28 15:49:00",
        "amount": 375
    },
    {
        "timestamp": "2023-07-01 21:59:00",
        "amount": 620
    },
    {
        "timestamp": "2023-12-17 08:09:00",
        "amount": 480
    }
]


def get_transactions():
    """Helper to generate parsed transactions"""

    res = client.post(
        "/blackrock/challenge/v1/transactions:parse",
        json=expenses_payload
    )
    assert res.status_code == 200
    return res.json()


# -------------------------
# Test Parse
# -------------------------

def test_parse_transactions():

    res = client.post(
        "/blackrock/challenge/v1/transactions:parse",
        json=expenses_payload
    )

    assert res.status_code == 200
    data = res.json()

    assert len(data) == 4
    assert data[0]["ceiling"] == 300
    assert data[0]["remanent"] == 50


# -------------------------
# Test Validator
# -------------------------

def test_validator():

    transactions = get_transactions()

    payload = {
        "wage": 50000,
        "transactions": transactions
    }

    res = client.post(
        "/blackrock/challenge/v1/transactions:validator",
        json=payload
    )

    assert res.status_code == 200
    data = res.json()

    assert "valid" in data
    assert "invalid" in data
    assert len(data["valid"]) == 4


# -------------------------
# Test Temporal Filter
# -------------------------

def test_temporal_filter():

    transactions = get_transactions()

    payload = {
        "q": [
            {
                "fixed": 0,
                "start": "2023-07-01 00:00:00",
                "end": "2023-07-31 23:59:59"
            }
        ],
        "p": [
            {
                "extra": 25,
                "start": "2023-10-01 08:00:00",
                "end": "2023-12-31 19:59:59"
            }
        ],
        "k": [],
        "transactions": transactions
    }

    res = client.post(
        "/blackrock/challenge/v1/transactions:filter",
        json=payload
    )

    assert res.status_code == 200
    data = res.json()

    assert "valid" in data
    assert len(data["valid"]) == 4


# -------------------------
# Returns Payload Builder
# -------------------------

def build_returns_payload():

    transactions = get_transactions()

    return {
        "age": 29,
        "wage": 50000,
        "inflation": 0.055,
        "q": [
            {
                "fixed": 0,
                "start": "2023-07-01 00:00:00",
                "end": "2023-07-31 23:59:59"
            }
        ],
        "p": [
            {
                "extra": 25,
                "start": "2023-10-01 08:00:00",
                "end": "2023-12-31 19:59:59"
            }
        ],
        "k": [
            {
                "start": "2023-03-01 00:00:00",
                "end": "2023-11-30 23:59:59"
            },
            {
                "start": "2023-01-01 00:00:00",
                "end": "2023-12-31 23:59:59"
            }
        ],
        "transactions": transactions
    }


# -------------------------
# Test Returns NPS
# -------------------------

def test_returns_nps():

    payload = build_returns_payload()

    res = client.post(
        "/blackrock/challenge/v1/returns:nps",
        json=payload
    )

    assert res.status_code == 200
    data = res.json()

    assert "savingsByDates" in data
    assert len(data["savingsByDates"]) == 2


# -------------------------
# Test Returns Index
# -------------------------

def test_returns_index():

    payload = build_returns_payload()

    res = client.post(
        "/blackrock/challenge/v1/returns:index",
        json=payload
    )

    assert res.status_code == 200
    data = res.json()

    assert "savingsByDates" in data
    assert len(data["savingsByDates"]) == 2


# -------------------------
# Test Performance
# -------------------------

def test_performance():

    res = client.get(
        "/blackrock/challenge/v1/performance"
    )

    assert res.status_code == 200

    data = res.json()

    assert "time" in data
    assert "memory" in data
    assert "threads" in data