import pandas as pd
import os

print("\n--- PRE-CLEANING STARTED ---\n")

# -----------------------------------
# Setup base path (robust)
# -----------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

clinical_path = os.path.join(BASE_DIR, "data/curated/patient_features_semantic.csv")
behavior_path = os.path.join(BASE_DIR, "data/raw/food_logs.csv")
health_path   = os.path.join(BASE_DIR, "data/raw/user_health_data.csv")

# -----------------------------------
# Load datasets
# -----------------------------------

clinical = pd.read_csv(clinical_path)
behavior = pd.read_csv(behavior_path)
health   = pd.read_csv(health_path)

# -----------------------------------
# CLINICAL CLEANING
# -----------------------------------

print("Cleaning clinical data...")

num_cols = ["glucose","hba1c","triglycerides","creatinine","bmi","weight"]
clinical[num_cols] = clinical[num_cols].apply(pd.to_numeric, errors="coerce")

clinical = clinical.drop_duplicates(subset=["patient_id"])

# -----------------------------------
# BEHAVIOR CLEANING
# -----------------------------------

print("Cleaning behavioral data...")

behavior = behavior.dropna(subset=["patient_id"])
behavior["calories"] = pd.to_numeric(behavior["calories"], errors="coerce")
behavior = behavior[behavior["calories"] > 0]

# -----------------------------------
# HEALTH CLEANING
# -----------------------------------

print("Cleaning lifestyle data...")

health = health.drop_duplicates(subset=["patient_id"])

num_cols_health = ["glucose","hba1c","bmi","stress_level","sleep_hours","craving_level"]
health[num_cols_health] = health[num_cols_health].apply(pd.to_numeric, errors="coerce")

# -----------------------------------
# Save cleaned files
# -----------------------------------

output_dir = os.path.join(BASE_DIR, "data/curated")

clinical.to_csv(os.path.join(output_dir, "clinical_clean.csv"), index=False)
behavior.to_csv(os.path.join(output_dir, "behavior_clean.csv"), index=False)
health.to_csv(os.path.join(output_dir, "health_clean.csv"), index=False)

print("\n--- PRE-CLEANING DONE ---")
