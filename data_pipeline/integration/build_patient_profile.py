import pandas as pd
import os

print("\n--- BUILDING UNIFIED PATIENT PROFILES ---\n")

# -----------------------------------
# Setup base directory
# -----------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# -----------------------------------
# Paths
# -----------------------------------

clinical_path = os.path.join(BASE_DIR, "data/curated/clinical_clean.csv")
behavior_path = os.path.join(BASE_DIR, "data/curated/behavior_clean.csv")
health_path   = os.path.join(BASE_DIR, "data/curated/health_clean.csv")

# -----------------------------------
# Load data
# -----------------------------------

clinical = pd.read_csv(clinical_path)
behavior = pd.read_csv(behavior_path)
health   = pd.read_csv(health_path)

# -----------------------------------
# Behavioral aggregation
# -----------------------------------

print("Aggregating behavioral data...")

behavior_summary = behavior.groupby("patient_id").agg({
    "calories": "mean",
    "food_type": "count"
}).reset_index()

behavior_summary.rename(columns={
    "food_type": "craving_frequency",
    "calories": "avg_craving_calories"
}, inplace=True)

# -----------------------------------
# Merge datasets
# -----------------------------------

print("Merging datasets...")

merged = clinical.merge(health, on="patient_id", how="left")
merged = merged.merge(behavior_summary, on="patient_id", how="left")

# -----------------------------------
# Resolve feature conflicts
# -----------------------------------

print("Resolving feature conflicts...")

def unify(primary, secondary):
    return primary.combine_first(secondary)

if "glucose_x" in merged.columns:
    merged["glucose"] = unify(merged["glucose_x"], merged["glucose_y"])
    merged["hba1c"]   = unify(merged["hba1c_x"], merged["hba1c_y"])
    merged["bmi"]     = unify(merged["bmi_x"], merged["bmi_y"])

    merged.drop(columns=[
        "glucose_x", "glucose_y",
        "hba1c_x", "hba1c_y",
        "bmi_x", "bmi_y"
    ], inplace=True)

# -----------------------------------
# Handle missing values (REALISTIC)
# -----------------------------------

print("Handling missing values...")

# Fill clinical values (important for modeling / reasoning)
clinical_cols = ["glucose", "hba1c", "triglycerides", "creatinine", "bmi", "weight"]

for col in clinical_cols:
    if col in merged.columns:
        merged[col] = merged[col].fillna(merged[col].median())

# Semantic label → "None" means no detected condition
merged["snomed_condition"] = merged["snomed_condition"].astype(str)
merged["snomed_condition"] = merged["snomed_condition"].replace("nan", "None")

# -----------------------------------
# Post-clean
# -----------------------------------

merged["avg_craving_calories"] = merged["avg_craving_calories"].fillna(0)
merged["craving_frequency"]    = merged["craving_frequency"].fillna(0)

merged = merged.drop_duplicates(subset=["patient_id"])

# -----------------------------------
# Save output
# -----------------------------------

output_path = os.path.join(BASE_DIR, "data/semantic_ready/patient_dataset.csv")

os.makedirs(os.path.dirname(output_path), exist_ok=True)
merged.to_csv(output_path, index=False)

print("\n--- INTEGRATION COMPLETE ---")
print(f"Saved to: {output_path}")
