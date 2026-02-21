# BlackRock Auto-Saving Challenge

**Author:** Gaurav Surolia

---

## 📌 Overview

Retirement planning in emerging markets often suffers from low savings rates due to behavioral and operational friction. This project implements a production-grade API system that enables automated retirement savings using expense-based micro-investments with temporal constraints and financial return projections.

The system processes financial transactions, applies temporal investment rules, calculates investment returns across multiple financial instruments, and provides inflation-adjusted projections.

The solution is fully containerized using Docker and designed with scalability, performance, and enterprise-grade engineering practices.

---

## 🏗️ Architecture

The system follows a modular service-oriented architecture:

```
app/
 ├── main.py              # FastAPI entry point
 ├── parser.py            # Transaction parsing logic
 ├── validator.py         # Transaction validation
 ├── temporal.py          # Temporal rule processing
 ├── investment.py        # Financial returns calculation
 ├── performance.py       # System metrics
 └── models.py            # Data models
```

Processing Pipeline:

1. Transaction Parsing
2. Transaction Validation
3. Temporal Constraints Application (q, p, k rules)
4. Savings Aggregation
5. Investment Returns Calculation
6. Performance Reporting

---

## ⚙️ Processing Logic

### Step 1 — Ceiling & Remanent Calculation

Each expense is rounded to the next multiple of 100:

```
ceiling = ceil(amount / 100) * 100
remanent = ceiling - amount
```

The remanent represents the auto-invested micro-saving.

---

### Step 2 — q Period Rules (Fixed Override)

If a transaction falls within a q period:

* Remanent is replaced with the fixed value
* If multiple periods match → latest start date is selected

---

### Step 3 — p Period Rules (Extra Addition)

If a transaction falls within p periods:

* All matching extra values are added
* p rules are cumulative and applied after q rules

---

### Step 4 — k Period Aggregation

Transactions are grouped into evaluation windows:

* A transaction may belong to multiple k periods
* Each k period is evaluated independently

---

### Step 5 — Investment Returns

Two investment instruments are supported:

| Instrument | Rate            | Constraints          |
| ---------- | --------------- | -------------------- |
| NPS        | 7.11% annually  | Tax rebate up to ₹2L |
| Index Fund | 14.49% annually | No limits            |

Compound interest:

```
A = P × (1 + r)^t
```

Inflation adjustment:

```
Real = A / (1 + inflation)^t
```

---

### Step 6 — NPS Tax Benefit

```
Deduction = min(invested, 10% annual income, ₹2,00,000)

Tax Benefit = Tax(income) − Tax(income − deduction)
```

Simplified Indian tax slabs are implemented as per requirements.

---

## 🚀 API Endpoints

Base URL:

```
http://localhost:5477/blackrock/challenge/v1
```

### 1️⃣ Parse Transactions

```
POST /transactions:parse
```

Converts expenses into enriched transactions with ceiling and remanent.

---

### 2️⃣ Validate Transactions

```
POST /transactions:validator
```

Returns valid and invalid transactions.

---

### 3️⃣ Temporal Filter

```
POST /transactions:filter
```

Applies q and p temporal constraints.

---

### 4️⃣ Returns Calculation

```
POST /returns:nps
POST /returns:index
```

Calculates investment projections and savings grouped by k periods.

---

### 5️⃣ Performance Metrics

```
GET /performance
```

Returns:

* Execution time
* Memory usage
* Active threads

---

## 🐳 Docker Deployment

### Build Image

```
docker build -t blk-hacking-ind-gaurav-surolia .
```

### Run Container

```
docker run -d -p 5477:5477 blk-hacking-ind-gaurav-surolia
```

## Docker Image

Public image available at:

docker pull gauravsurolia/blk-hacking-ind-gaurav-surolia

Run:

docker run -p 5477:5477 gauravsurolia/blk-hacking-ind-gaurav-surolia

### Access API

```
http://localhost:5477/docs
```

---

## 💻 Local Development

Install dependencies:

```
pip install -r requirements.txt
```

Run server:

```
python -m uvicorn app.main:app --host 0.0.0.0 --port 5477
```

---

## 🧪 Testing

Tests are implemented using **pytest**.

Run:

```
pytest -v
```

Test coverage includes:

* Parsing logic
* Validation
* Temporal rules
* Returns calculations
* Performance endpoint

---

## 📊 Performance Strategy

The system is designed to handle up to **1 million transactions and temporal rules**.

Key considerations:

* Efficient timestamp comparisons
* Minimal memory overhead
* Linear iteration for transaction processing
* Predictable computational complexity
* Containerized execution environment

---

## 📈 Assumptions

* All timestamps follow `YYYY-MM-DD HH:mm:ss`
* Inflation rate provided as decimal (e.g., 0.055)
* Age below 60 unless specified
* Investment compounding occurs annually
* Transactions are within a single calendar year
* No external financial APIs are required

---

## 🔮 Future Improvements

Potential enhancements:

* Interval tree indexing for temporal rules
* Async batch processing for large datasets
* Database persistence layer
* Authentication & authorization
* Kubernetes deployment support
* CI/CD automation pipeline
* Observability with Prometheus & Grafana

---

## 🎥 Demo

Swagger UI available at:

```
http://localhost:5477/docs
```

---

## 📦 Submission Notes

* Application runs on port **5477** inside container
* Linux-based Docker image used
* Image naming follows challenge convention
* All required endpoints implemented
* Tests included as bonus

---

## 👨‍💻 Author

**Gaurav Surolia**
Python Developer | Backend Engineer

---
