"""Telco churn SQL analysis. Usage: python sql_analysis.py path/to/telco.csv"""
import sys, sqlite3
import pandas as pd

csv = sys.argv[1] if len(sys.argv) > 1 else "telco.csv"
df = pd.read_csv(csv)
need = {"Contract", "Churn", "tenure", "MonthlyCharges", "PaymentMethod"}
missing = need - set(df.columns)
if missing:
    sys.exit(f"CSV me yeh columns nahi mile: {sorted(missing)}. Apne columns ke naam bhejein.")

con = sqlite3.connect("telco.db")
df.to_sql("customers", con, if_exists="replace", index=False)

QUERIES = {
"Q1 Churn rate by contract type (GROUP BY)": """
SELECT Contract,
       COUNT(*) AS customers,
       SUM(Churn = 'Yes') AS churned,
       ROUND(100.0 * SUM(Churn = 'Yes') / COUNT(*), 1) AS churn_pct
FROM customers
GROUP BY Contract
ORDER BY churn_pct DESC;""",

"Q2 Payment methods with churn above 25% (HAVING)": """
SELECT PaymentMethod,
       COUNT(*) AS customers,
       ROUND(100.0 * SUM(Churn = 'Yes') / COUNT(*), 1) AS churn_pct
FROM customers
GROUP BY PaymentMethod
HAVING churn_pct > 25
ORDER BY churn_pct DESC;""",

"Q3 Churn by tenure band (CASE)": """
SELECT CASE WHEN tenure < 12 THEN '0-11 months'
            WHEN tenure < 24 THEN '12-23 months'
            WHEN tenure < 48 THEN '24-47 months'
            ELSE '48+ months' END AS tenure_band,
       COUNT(*) AS customers,
       ROUND(100.0 * SUM(Churn = 'Yes') / COUNT(*), 1) AS churn_pct
FROM customers
GROUP BY tenure_band
ORDER BY MIN(tenure);""",

"Q4 Rank contracts by average monthly charges (window function)": """
SELECT Contract,
       ROUND(AVG(MonthlyCharges), 2) AS avg_monthly,
       RANK() OVER (ORDER BY AVG(MonthlyCharges) DESC) AS charge_rank
FROM customers
GROUP BY Contract;""",

"Q5 Churned customers paying above average (subquery)": """
SELECT COUNT(*) AS high_paying_churners,
       ROUND(AVG(MonthlyCharges), 2) AS avg_charge_of_them
FROM customers
WHERE Churn = 'Yes'
  AND MonthlyCharges > (SELECT AVG(MonthlyCharges) FROM customers);""",
}

with open("queries.sql", "w") as f:
    for title, q in QUERIES.items():
        f.write(f"-- {title}{q}\n\n")
        print(f"\n== {title} ==")
        print(pd.read_sql(q, con).to_string(index=False))
con.close()