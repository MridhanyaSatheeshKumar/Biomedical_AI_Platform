import pandas as pd
import os

print("\nBuilding unified patient profiles...\n")

# -----------------------------------
# Setup base directory (robust paths)
# -----------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

clinical_path = os.path.join(
    BASE_DIR,
    "FHIR_Project/data/patient_features_semantic.csv"
)

behavior_path = os.path.join(
    BASE_DIR,
    "Food_Craving_Pattern_Analysis/data/food_logs.csv"
)

health_path = os.path.join(
    BASE_DIR,
    "Personalized_Nutrition_AI/data/user_health_data.csv"
)

# -----------------------------------
# Check required files exist
# -----------------------------------

if not os.path.exists(clinical_path):
    raise Exception(
        "Missing patient_features_semantic.csv. Run FHIR pipeline first."
    )

# -----------------------------------
# Load data
# -----------------------------------

clinical = pd.read_csv(clinical_path)
behavior = pd.read_csv(behavior_path)
health = pd.read_csv(health_path)

# -----------------------------------
# Normalize ID types (string)
# -----------------------------------

clinical["patient_id"] = clinical["patient_id"].astype(str)
behavior["user_id"] = behavior["user_id"].astype(str)
health["user_id"] = health["user_id"].astype(str)

# -----------------------------------
# Entity Mapping (FHIR → user_id)
# -----------------------------------

unique_patients = clinical["patient_id"].unique()
available_users = health["user_id"].unique()

mapping = pd.DataFrame({
    "patient_id": unique_patients[:len(available_users)],
    "user_id": available_users
})

# Merge mapping into clinical data
clinical = clinical.merge(mapping, on="patient_id", how="left")

# Drop patients without mapping
clinical = clinical.dropna(subset=["user_id"])

# -----------------------------------
# Behavioral feature engineering
# -----------------------------------

behavior_summary = behavior.groupby("user_id").agg({

    "calories": "mean",

    "food_type": "count"

}).reset_index()

behavior_summary.rename(
    columns={
        "food_type": "craving_frequency",
        "calories": "avg_craving_calories"
    },
    inplace=True
)

# -----------------------------------
# Merge datasets
# -----------------------------------

merged = clinical.merge(
    health,
    on="user_id",
    how="left"
)

merged = merged.merge(
    behavior_summary,
    on="user_id",
    how="left"
)

# -----------------------------------
# Save output
# -----------------------------------

output_path = os.path.join(
    BASE_DIR,
    "Integration/patient_integrated_profile.csv"
)

merged.to_csv(output_path, index=False)

print("Patient integrated profiles created successfully")
print(f"Saved to: {output_path}")
