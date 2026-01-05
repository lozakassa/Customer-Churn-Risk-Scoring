DROP TABLE IF EXISTS features_customer;

CREATE TABLE features_customer AS
SELECT
    customer_id,
    -- Tenure flags
	CASE WHEN tenure < 12 THEN 1 ELSE 0 END AS tenure_0_1yr,
	CASE WHEN tenure >= 12 AND tenure < 24 THEN 1 ELSE 0 END AS tenure_1_2yr,
	CASE WHEN tenure >= 24 AND tenure < 48 THEN 1 ELSE 0 END AS tenure_2_4yr,
	CASE WHEN tenure >= 48 THEN 1 ELSE 0 END AS tenure_4yr_plus,

    monthly_charges,
    total_charges,
	
	-- High monthly charge flag
    CASE WHEN monthly_charges >= 80 THEN 1 ELSE 0 END AS high_monthly_charge,
	
    -- Contract type flags
    CASE WHEN contract = 'Month-to-month' THEN 1 ELSE 0 END AS is_month_to_month,
    CASE WHEN contract = 'One year' THEN 1 ELSE 0 END AS is_one_year,
    CASE WHEN contract = 'Two year' THEN 1 ELSE 0 END AS is_two_year,

    -- Payment method flags
    CASE WHEN payment_method = 'Electronic check' THEN 1 ELSE 0 END AS pay_electronic_check,
    CASE WHEN payment_method = 'Mailed check' THEN 1 ELSE 0 END AS pay_mailed_check,
    CASE WHEN payment_method = 'Bank transfer (automatic)' THEN 1 ELSE 0 END AS pay_bank_transfer,
    CASE WHEN payment_method = 'Credit card (automatic)' THEN 1 ELSE 0 END AS pay_credit_card,
	
	

    churn
FROM clean_churn;

