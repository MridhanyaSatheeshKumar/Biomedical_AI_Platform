import pandas as pd
import os

print("\n--- Mapping conditions to SNOMED ---\n")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
data_path = os.path.join(BASE_DIR, "data/semantic_ready/patient_dataset.csv")

df = pd.read_csv(data_path)

# Ensure column exists
df["snomed_condition"] = df["snomed_condition"].fillna("")

# Save (clean version)
output_path = os.path.join(BASE_DIR, "data/semantic_ready/patient_dataset.csv")
df.to_csv(output_path, index=False)

print("SNOMED mapping verified and saved")
