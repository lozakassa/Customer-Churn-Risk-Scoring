# 📊 Customer Churn Risk Scoring & Validation

## 🔍 Overview

This repository contains an end-to-end **customer churn risk scoring project** focused on identifying and ranking customers by their likelihood of churn using an **interpretable logistic regression model**.

🎯 **Primary objective**:

* Separate **high-risk** customers from **low-risk** customers
* Support **operational decision-making** (retention targeting)

This project prioritizes **risk ranking, validation, and interpretability** over black-box prediction.

---

## 🗂️ Data

### 📥 Raw Data

```text
WA_Fn-UseC_-Telco-Customer-Churn.csv
```

📌 Customer-level dataset containing:

* 🧾 Tenure information
* 📄 Contract type
* 💳 Payment method
* 💰 Monthly and total charges
* 🚪 Churn indicator (binary)

---

## 🧹 Data Preparation (SQL)

All data cleaning and feature engineering were completed in SQL before modeling.

### 🛠️ SQL Scripts

```text
sql/
 ├── 01_clean_churn.sql
 └── 02_features_churn.sql
```

🔹 **01_clean_churn.sql**

* 🧼 Handles missing values
* 🔄 Standardizes fields
* 🧱 Creates a clean base customer table

🔹 **02_features_churn.sql**

* ⏳ Creates tenure group indicators
* 📑 Generates contract-type flags
* 💳 Encodes payment methods
* 💵 Produces pricing features

### 📦 Final Modeling Dataset

```text
data/processed/features_customer.csv
```

---

## 📈 Exploratory Data Analysis

### 📊 Tableau

```text
dashboards/tableau/Descriptive EDA.twb
```

Used to explore:

* 📉 Churn rate by tenure
* 🧾 Churn by contract type
* 💰 Pricing distributions

### 📊 Power BI

```text
dashboards/powerbi/Churn dashboard.pbix
```

Interactive dashboard highlighting:

* 📌 Overall churn rate
* 🧩 Churn by contract
* 📈 Churn by tenure and pricing bands

---

## 🤖 Modeling Approach

### 🧠 Model Selection

A **logistic regression model** was selected as the primary **risk-separating model** due to:

* ✅ Interpretability
* 🏢 Industry acceptance
* 📐 Ability to generate continuous risk scores

### 🧪 Models Evaluated

```text
Model 1: Core Features
- Tenure indicators
- Contract type
- Payment method

Model 2: Core + Pricing (Final Model)
- All core features
- Monthly charges
- Total charges
```

🏆 **Final model**: Core + Pricing Logistic Regression

---

## 🐍 Python Implementation

```text
src/module1.py
```

Key steps:

```python
# Train logistic regression model
logit_m2.fit(X_train, y_train)

# Generate churn risk scores
p_churn = logit_m2.predict_proba(X_test)[:, 1]
```

📤 Output:

* `p_churn` → continuous churn **risk score** used for ranking customers

---

## ✅ Model Validation

Validation was performed on a **held-out test set** using industry-standard metrics.

### 📐 ROC AUC

* Confirms strong ranking and discrimination ability

### 📊 Gains & Deciles

* 🔝 **Top 20%** of customers capture **~46% of churn events**
* Demonstrates strong concentration of churn risk

### 📏 KS Statistic

* **KS ≈ 0.50**
* Indicates strong separation between churners and non-churners
* Confirms the model’s effectiveness as a risk-separating tool

---

## 🧩 Risk Segmentation

To enhance interpretability, **risk bands** were created on top of model scores.

🔸 **Monthly Charges**

* Low / Medium / High

🔸 **Tenure**

* Early / Mid / Long

🔸 **Contract Type**

* Month-to-month / One-year / Two-year

⚠️ These bands are **descriptive layers**, not separate predictive models.

---

## 🔑 Key Findings

* 🚨 Month-to-month customers show the highest churn risk
* ⏱️ Early-tenure customers are significantly more likely to churn
* 💸 Higher monthly charges are associated with increased churn probability
* 🎯 A small subset of customers accounts for a large share of churn

---

## 🗃️ Repository Structure

```text
customer-churn-risk-scoring/
 ├── data/
 │    ├── raw/
 │    └── processed/
 ├── sql/
 │    ├── 01_clean_churn.sql
 │    └── 02_features_churn.sql
 ├── src/
 │    └── module1.py
 ├── dashboards/
 │    ├── tableau/
 │    │    └── Descriptive EDA.twb
 │    └── powerbi/
 │         └── Churn dashboard.pbix
 └── README.md
```

---

## 🧰 Tools Used

```text
🧮 SQL
🐍 Python (pandas, scikit-learn, matplotlib)
📊 Tableau
📊 Power BI
```

---

## 📝 Notes

This project emphasizes **risk ranking, validation, and interpretability** rather than black-box prediction. The workflow reflects common industry practices in churn and risk analytics.

