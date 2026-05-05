import pandas as pd
import os

print("\n--- Running data quality checks ---\n")

# -----------------------------------
# Setup path
# -----------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
data_path = os.path.join(BASE_DIR, "data/semantic_ready/patient_dataset.csv")

df = pd.read_csv(data_path)

# -----------------------------------
# 1. Missing values
# -----------------------------------

print("Missing values per column:\n")
missing = df.isnull().sum()
print(missing)

# -----------------------------------
# 2. Outlier detection
# -----------------------------------

print("\nChecking clinical ranges:\n")

if "glucose" in df.columns:
    high_glucose = df[df["glucose"] > 300]
    print("Extreme glucose (>300):", len(high_glucose))

if "bmi" in df.columns:
    high_bmi = df[df["bmi"] > 60]
    print("Extreme BMI (>60):", len(high_bmi))

if "triglycerides" in df.columns:
    high_trig = df[df["triglycerides"] > 1000]
    print("Extreme triglycerides:", len(high_trig))

# -----------------------------------
# 3. Negative values
# -----------------------------------

numeric_cols = df.select_dtypes(include=['float64','int64'])

negative = (numeric_cols < 0).sum().sum()
print("\nTotal negative values:", negative)

# -----------------------------------
# 4. Duplicate check
# -----------------------------------

if "patient_id" in df.columns:
    duplicates = df["patient_id"].duplicated().sum()
    print("Duplicate patient IDs:", duplicates)

# -----------------------------------
# Save report
# -----------------------------------

report_path = os.path.join(BASE_DIR, "data/data_quality_report.csv")
missing.to_frame(name="missing_count").to_csv(report_path)

print("\nData quality validation complete.")
print(f"Report saved to: {report_path}")
