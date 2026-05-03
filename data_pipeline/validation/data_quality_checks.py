import pandas as pd

print("\nRunning data quality checks...\n")

# Load final dataset
df = pd.read_csv("data/patient_integrated_profile.csv")

# -------------------------------
# 1. Missing values
# -------------------------------
print("Missing values per column:\n")
missing = df.isnull().sum()
print(missing)

# -------------------------------
# 2. Outlier detection
# -------------------------------
print("\nChecking clinical ranges:\n")

if "glucose_y" in df.columns:
    high_glucose = df[df["glucose_y"] > 300]
    print("Extreme glucose (>300):", len(high_glucose))

if "bmi_y" in df.columns:
    high_bmi = df[df["bmi_y"] > 60]
    print("Extreme BMI (>60):", len(high_bmi))

if "triglycerides" in df.columns:
    high_trig = df[df["triglycerides"] > 1000]
    print("Extreme triglycerides:", len(high_trig))

# -------------------------------
# 3. Negative values
# -------------------------------
numeric_cols = df.select_dtypes(include=['float64','int64'])

negative = (numeric_cols < 0).sum().sum()

print("\nTotal negative values:", negative)

# -------------------------------
# 4. Duplicate check
# -------------------------------
if "patient_id" in df.columns:
    duplicates = df["patient_id"].duplicated().sum()
    print("Duplicate patient IDs:", duplicates)

# -------------------------------
# Save report
# -------------------------------
report = missing.to_frame(name="missing_count")
report.to_csv("data/data_quality_report.csv")

print("\nData quality validation complete.")
print("Validation report saved.")
