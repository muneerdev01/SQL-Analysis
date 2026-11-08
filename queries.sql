-- Q1 Churn rate by contract type (GROUP BY)
SELECT Contract,
       COUNT(*) AS customers,
       SUM(Churn = 'Yes') AS churned,
       ROUND(100.0 * SUM(Churn = 'Yes') / COUNT(*), 1) AS churn_pct
FROM customers
GROUP BY Contract
ORDER BY churn_pct DESC;

-- Q2 Payment methods with churn above 25% (HAVING)
SELECT PaymentMethod,
       COUNT(*) AS customers,
       ROUND(100.0 * SUM(Churn = 'Yes') / COUNT(*), 1) AS churn_pct
FROM customers
GROUP BY PaymentMethod
HAVING churn_pct > 25
ORDER BY churn_pct DESC;

-- Q3 Churn by tenure band (CASE)
SELECT CASE WHEN tenure < 12 THEN '0-11 months'
            WHEN tenure < 24 THEN '12-23 months'
            WHEN tenure < 48 THEN '24-47 months'
            ELSE '48+ months' END AS tenure_band,
       COUNT(*) AS customers,
       ROUND(100.0 * SUM(Churn = 'Yes') / COUNT(*), 1) AS churn_pct
FROM customers
GROUP BY tenure_band
ORDER BY MIN(tenure);

-- Q4 Rank contracts by average monthly charges (window function)
SELECT Contract,
       ROUND(AVG(MonthlyCharges), 2) AS avg_monthly,
       RANK() OVER (ORDER BY AVG(MonthlyCharges) DESC) AS charge_rank
FROM customers
GROUP BY Contract;

-- Q5 Churned customers paying above average (subquery)
SELECT COUNT(*) AS high_paying_churners,
       ROUND(AVG(MonthlyCharges), 2) AS avg_charge_of_them
FROM customers
WHERE Churn = 'Yes'
  AND MonthlyCharges > (SELECT AVG(MonthlyCharges) FROM customers);

