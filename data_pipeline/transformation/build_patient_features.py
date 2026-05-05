import os
import pandas as pd

# -----------------------------------
# Setup paths
# -----------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

INPUT_PATH = os.path.join(BASE_DIR, "data", "staging", "metabolic_biomarkers.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "curated", "patient_features_semantic.csv")

# -----------------------------------
# Load data
# -----------------------------------

df = pd.read_csv(INPUT_PATH)

df["observation_date"] = pd.to_datetime(df["observation_date"], errors="coerce", utc=True)

print("\n--- Building Patient Features ---\n")

# -----------------------------------
# Helper functions
# -----------------------------------

def get_mean_feature(data, test_name, feature_name):
    subset = data[data["test_name"] == test_name]
    return subset.groupby("patient_id")["value"].mean().rename(feature_name)

def get_latest_feature(data, test_name, feature_name):
    subset = data[data["test_name"] == test_name]
    latest = subset.sort_values("observation_date").groupby("patient_id").tail(1)
    return latest.set_index("patient_id")["value"].rename(feature_name)

# -----------------------------------
# Feature extraction
# -----------------------------------

features = []

features.append(get_mean_feature(df, "Glucose", "glucose"))
features.append(get_latest_feature(df, "HbA1c", "hba1c"))
features.append(get_mean_feature(df, "Triglycerides", "triglycerides"))
features.append(get_mean_feature(df, "Creatinine", "creatinine"))
features.append(get_latest_feature(df, "BMI", "bmi"))
features.append(get_latest_feature(df, "Body Weight", "weight"))

# -----------------------------------
# Combine all features
# -----------------------------------

patient_df = pd.concat(features, axis=1).reset_index()

# -----------------------------------
# Risk rules (simple clinical logic)
# -----------------------------------

print("Applying clinical rules...")

patient_df["glycemic_risk_rule"] = (
    (patient_df["glucose"] > 126) | (patient_df["hba1c"] > 6.5)
).astype(int)

patient_df["obesity_risk"] = (patient_df["bmi"] > 30).astype(int)

patient_df["lipid_risk"] = (patient_df["triglycerides"] > 150).astype(int)

# -----------------------------------
# Map to condition labels
# -----------------------------------

def map_condition(row):
    if row["glycemic_risk_rule"]:
        return "Diabetes Mellitus"
    elif row["obesity_risk"]:
        return "Obesity"
    elif row["lipid_risk"]:
        return "Hyperlipidemia"
    return "None"

patient_df["snomed_condition"] = patient_df.apply(map_condition, axis=1)

# -----------------------------------
# Save output
# -----------------------------------

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
patient_df.to_csv(OUTPUT_PATH, index=False)

print("\n--- Feature Engineering Complete ---")
print(f"Saved to: {OUTPUT_PATH}")
