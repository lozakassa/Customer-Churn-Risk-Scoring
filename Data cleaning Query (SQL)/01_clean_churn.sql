DROP TABLE IF EXISTS clean_churn;

CREATE TABLE clean_churn AS
SELECT
    customerID AS customer_id,
    gender,
    CAST(SeniorCitizen AS INTEGER) AS senior_citizen,
    CASE WHEN Partner = 'Yes' THEN 1 ELSE 0 END AS has_partner,
    CASE WHEN Dependents = 'Yes' THEN 1 ELSE 0 END AS has_dependents,
    CAST(tenure AS INTEGER) AS tenure,
    CAST(MonthlyCharges AS REAL) AS monthly_charges,
    CAST(NULLIF(TotalCharges, '') AS REAL) AS total_charges,
    Contract AS contract,
    PaymentMethod AS payment_method,
    CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END AS churn
FROM raw_churn;