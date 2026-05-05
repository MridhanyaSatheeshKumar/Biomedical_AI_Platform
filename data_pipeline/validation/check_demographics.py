import json
import os
import pandas as pd
from datetime import datetime

FHIR_PATH = "data/intermediate/fhir"

patients = []

for file in os.listdir(FHIR_PATH):
    if file.endswith(".json"):
        with open(os.path.join(FHIR_PATH, file)) as f:
            data = json.load(f)

        for entry in data.get("entry", []):
            resource = entry.get("resource", {})

            if resource.get("resourceType") == "Patient":
                patients.append({
                    "patient_id": resource.get("id"),
                    "gender": resource.get("gender"),
                    "birthDate": resource.get("birthDate")
                })

df = pd.DataFrame(patients)

print("\nTotal patients:", len(df))

df["birthDate"] = pd.to_datetime(df["birthDate"], errors="coerce")
df["age"] = datetime.now().year - df["birthDate"].dt.year

print("\nGender distribution:")
print(df["gender"].value_counts())

print("\nAge summary:")
print(df["age"].describe())

df.to_csv("data/processed/patient_demographics.csv", index=False)
