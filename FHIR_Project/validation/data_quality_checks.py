import pandas as pd

df = pd.read_csv("data/patient_features.csv")

print("\nRunning data quality checks...\n")

# Missing values check
missing = df.isnull().sum()

print("Missing values per column:")
print(missing)

# Outlier detection (simple clinical thresholds)

print("\nChecking clinical ranges:")

if "glucose" in df:
    high_glucose = df[df["glucose"] > 300]

    print("Extreme glucose values (>300):", len(high_glucose))

if "bmi" in df:
    high_bmi = df[df["bmi"] > 60]

    print("Extreme BMI values (>60):", len(high_bmi))

if "triglycerides" in df:
    high_trig = df[df["triglycerides"] > 1000]

    print("Extreme triglycerides:", len(high_trig))


# Negative value check

negative = df[(df.select_dtypes(include=['float64','int64']) < 0).any(axis=1)]

print("\nNegative value rows:", len(negative))


print("\nData quality validation complete.")

report = missing.to_frame(name="missing_count")

report.to_csv("data/data_quality_report.csv")

print("Validation report saved.")
