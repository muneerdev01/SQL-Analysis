# SQL Churn Analysis

SQL analysis of the IBM Telco Customer Churn dataset (7,043 customers) using Python, SQLite, and Pandas.

## Files
- `sql_analysis.py` loads the CSV into SQLite and runs 5 queries
- `queries.sql` the 5 queries
- `WA_Fn-UseC_-Telco-Customer-Churn.csv` the dataset

## How to run
```
pip install pandas
python sql_analysis.py WA_Fn-UseC_-Telco-Customer-Churn.csv
```

## Queries and findings

| # | SQL technique | Question | Finding |
|---|---|---|---|
| 1 | GROUP BY | Churn rate by contract type | Month-to-month 42.7%, one year 11.3%, two year 2.8% |
| 2 | HAVING | Payment methods with churn above 25% | Only electronic check qualifies (45.3%) |
| 3 | CASE | Churn by tenure band | 0-11 months 48.3%, 12-23 months 29.5%, 24-47 months 20.9%, 48+ months 9.6% |
| 4 | Window function (RANK) | Contracts ranked by average monthly charge | Month-to-month highest ($66.40), two year lowest ($60.77) |
| 5 | Subquery | Churned customers paying above the average charge | 1,355 of 1,869 churned customers; their average charge is $87.50 |

## Takeaway
Churn is concentrated among new customers on month-to-month contracts who pay by electronic check. Moving them to longer contracts is the clearest retention lever in this data.
