import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
import matplotlib.pyplot as plt


df = pd.read_csv(r"C:\Users\lozak\OneDrive\Desktop\Protfolio projects\Project 1\features_customer.csv")

print(df.head())


print(df.columns.tolist())
df.isna().sum().sort_values(ascending=False).head(10)
print("Churn rate:", df["churn"].mean())

df_clean = df[df['total_charges'].notna()].copy()

print(df_clean.shape)

print(df_clean.isna().sum())

features_core = [
    "tenure_0_1yr", "tenure_1_2yr", "tenure_2_4yr", "tenure_4yr_plus",
    "is_month_to_month", "is_one_year", "is_two_year",
    "pay_electronic_check", "pay_mailed_check", "pay_bank_transfer", "pay_credit_card"
]

features_pricing = ["monthly_charges", "total_charges"]

# Safety check: ensure columns exist
missing_cols = [c for c in (features_core + features_pricing + ["churn"]) if c not in df_clean.columns]
if missing_cols:
    raise ValueError(f"These columns are missing from your data: {missing_cols}")

# -----------------------------
# 4) TRAIN / TEST SPLIT
# -----------------------------
y = df_clean["churn"]

# Model 1 X
X1 = df_clean[features_core]

X1_train, X1_test, y_train, y_test = train_test_split(
    X1, y, test_size=0.30, random_state=42, stratify=y
)

# -----------------------------
# 5) MODEL 1: BASELINE LOGISTIC
# -----------------------------
logit_m1 = LogisticRegression(max_iter=1000, solver="liblinear")
logit_m1.fit(X1_train, y_train)

m1_probs = logit_m1.predict_proba(X1_test)[:, 1]
m1_auc = roc_auc_score(y_test, m1_probs)

coef_m1 = pd.DataFrame({
    "feature": X1_train.columns,
    "coef": logit_m1.coef_[0]
}).sort_values("coef", ascending=False)

print("\n=== MODEL 1 (Core) ===")
print("ROC AUC:", round(m1_auc, 4))
print(coef_m1.to_string(index=False))

# -----------------------------
# 6) MODEL 2: CORE + PRICING
# -----------------------------
X2 = df_clean[features_core + features_pricing]

X2_train, X2_test, y_train2, y_test2 = train_test_split(
    X2, y, test_size=0.30, random_state=42, stratify=y
)

logit_m2 = LogisticRegression(max_iter=1000, solver="liblinear")
logit_m2.fit(X2_train, y_train2)

m2_probs = logit_m2.predict_proba(X2_test)[:, 1]
m2_auc = roc_auc_score(y_test2, m2_probs)

coef_m2 = pd.DataFrame({
    "feature": X2_train.columns,
    "coef": logit_m2.coef_[0]
}).sort_values("coef", ascending=False)

print("\n=== MODEL 2 (Core + Pricing) ===")
print("ROC AUC:", round(m2_auc, 4))
print(coef_m2.to_string(index=False))

# ==========================================================
# 6) BUILD RISK BANDS + GAINS / DECILES USING MODEL 2 OUTPUT
# ==========================================================

# A) Scoring DataFrame on the TEST set used for Model 2
score_df = X2_test.copy().reset_index(drop=True)
score_df["actual_churn"] = pd.Series(y_test2).reset_index(drop=True)
score_df["p_churn"] = m2_probs

print("\nScore DF preview:")
print(score_df[["actual_churn", "p_churn"]].head())

# B) Risk Bands

# Monthly charges bands
def band_monthly_charges(x):
    if x < 40:
        return "Low"
    elif x < 80:
        return "Medium"
    else:
        return "High"

score_df["band_monthly_charges"] = score_df["monthly_charges"].apply(band_monthly_charges)

# Tenure bands (based on your one-hot tenure flags)
def band_tenure(row):
    if row["tenure_0_1yr"] == 1:
        return "High"
    elif row["tenure_1_2yr"] == 1:
        return "Medium"
    else:
        return "Low"

score_df["band_tenure"] = score_df.apply(band_tenure, axis=1)

# Contract bands (based on your one-hot contract flags)
def band_contract(row):
    if row["is_month_to_month"] == 1:
        return "High"
    elif row["is_one_year"] == 1:
        return "Medium"
    else:
        return "Low"

score_df["band_contract"] = score_df.apply(band_contract, axis=1)

print("\nBand counts:")
print("Monthly charges bands:\n", score_df["band_monthly_charges"].value_counts())
print("\nTenure bands:\n", score_df["band_tenure"].value_counts())
print("\nContract bands:\n", score_df["band_contract"].value_counts())

# C) Gains / Deciles table
# Decile 10 = highest risk, Decile 1 = lowest risk
score_df["decile"] = pd.qcut(score_df["p_churn"], 10, labels=False, duplicates="drop") + 1
score_df["decile"] = 11 - score_df["decile"]

gains = (
    score_df
    .groupby("decile")
    .agg(
        n=("actual_churn", "size"),
        churners=("actual_churn", "sum"),
        avg_p=("p_churn", "mean")
    )
    .sort_index(ascending=False)
)

gains["cum_churners"] = gains["churners"].cumsum()
gains["total_churners"] = gains["churners"].sum()
gains["cum_capture_rate"] = gains["cum_churners"] / gains["total_churners"]

print("\n=== Gains Table (Deciles) ===")
print(gains)

# D) Operational threshold selection (top X percent)
TOP_PCT = 0.20  # change to 0.10 for top 10%, 0.30 for top 30%, etc.

# Determine how many rows are in the top X%
n_top = int(np.ceil(TOP_PCT * len(score_df)))

# Rank by predicted risk
score_sorted = score_df.sort_values("p_churn", ascending=False).reset_index(drop=True)

# Threshold is the p_churn value at the cutoff position
threshold = float(score_sorted.loc[n_top - 1, "p_churn"])

# Flag customers above threshold
score_df["intervene_flag"] = (score_df["p_churn"] >= threshold).astype(int)

captured = int(score_df.loc[score_df["intervene_flag"] == 1, "actual_churn"].sum())
total = int(score_df["actual_churn"].sum())
capture_rate = captured / total if total > 0 else np.nan

print("\n=== Operational Threshold ===")
print(f"Top {int(TOP_PCT*100)}% cutoff probability threshold: {threshold:.4f}")
print(f"Churn captured in top {int(TOP_PCT*100)}%: {captured} / {total} ({capture_rate:.2%})")

# --------------------------------
# KS Curve (CORRECT ORDER)
# --------------------------------

ks_df = score_df.sort_values("p_churn", ascending=False).reset_index(drop=True)

ks_df["cum_churn"] = (
    ks_df["actual_churn"].cumsum()
    / ks_df["actual_churn"].sum()
)

ks_df["cum_nonchurn"] = (
    (1 - ks_df["actual_churn"]).cumsum()
    / (1 - ks_df["actual_churn"]).sum()
)

ks_df["ks"] = ks_df["cum_churn"] - ks_df["cum_nonchurn"]

ks_value = ks_df["ks"].max()
ks_index = ks_df["ks"].idxmax()

print("\n=== KS Statistic ===")
print("KS value:", round(float(ks_value), 4))

# --------------------------------
# KS Plot
# --------------------------------

plt.figure(figsize=(7, 5))

plt.plot(ks_df["cum_churn"], label="Cumulative Churners")
plt.plot(ks_df["cum_nonchurn"], label="Cumulative Non-Churners")

plt.vlines(
    x=ks_index,
    ymin=ks_df.loc[ks_index, "cum_nonchurn"],
    ymax=ks_df.loc[ks_index, "cum_churn"],
    colors="red",
    linestyles="dashed",
    label=f"KS = {ks_value:.3f}"
)

plt.title("KS Curve (Logistic Regression - Core + Pricing)")
plt.xlabel("Customers Sorted by Predicted Risk (High → Low)")
plt.ylabel("Cumulative Proportion")
plt.legend()
plt.tight_layout()
plt.show()