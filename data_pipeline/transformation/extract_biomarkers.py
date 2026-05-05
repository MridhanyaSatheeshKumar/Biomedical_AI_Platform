import os
import json
import pandas as pd

# -----------------------------------
# Setup base paths
# -----------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

FHIR_DIR = os.path.join(BASE_DIR, "data", "staging", "fhir")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "staging", "metabolic_biomarkers.csv")

# -----------------------------------
# LOINC ontology (temporary in-code mapping)
# -----------------------------------

LOINC_TERMINOLOGY = {
    "2339-0": {"concept_name": "Glucose", "category": "Metabolic Panel"},
    "4548-4": {"concept_name": "HbA1c", "category": "Diabetes Panel"},
    "2571-8": {"concept_name": "Triglycerides", "category": "Lipid Panel"},
    "38483-4": {"concept_name": "Creatinine", "category": "Renal Panel"},
    "6299-2": {"concept_name": "Urea Nitrogen", "category": "Renal Panel"},
    "2947-0": {"concept_name": "Sodium", "category": "Electrolyte Panel"},
    "6298-4": {"concept_name": "Potassium", "category": "Electrolyte Panel"},
    "39156-5": {"concept_name": "BMI", "category": "Vitals"},
    "29463-7": {"concept_name": "Body Weight", "category": "Vitals"}
}

# -----------------------------------
# Extract observations from FHIR
# -----------------------------------

def extract_observations(file_path):
    with open(file_path, "r") as f:
        bundle = json.load(f)

    records = []

    for entry in bundle.get("entry", []):
        resource = entry.get("resource", {})

        if resource.get("resourceType") != "Observation":
            continue

        # Patient ID
        patient_ref = resource.get("subject", {}).get("reference", "")
        patient_id = patient_ref.split("/")[-1]

        # LOINC code
        coding = resource.get("code", {}).get("coding", [])
        loinc_code = None

        for c in coding:
            if "loinc.org" in c.get("system", ""):
                loinc_code = c.get("code")
                break

        if not loinc_code:
            continue

        # Value
        value = resource.get("valueQuantity", {}).get("value")
        unit = resource.get("valueQuantity", {}).get("unit")

        # Date
        date = resource.get("effectiveDateTime")

        # -----------------------------------
        # Enrich using ontology
        # -----------------------------------

        concept_info = LOINC_TERMINOLOGY.get(loinc_code, {})

        records.append({
            "patient_id": patient_id,
            "loinc_code": loinc_code,
            "test_name": concept_info.get("concept_name"),
            "category": concept_info.get("category"),
            "value": value,
            "unit": unit,
            "observation_date": date
        })

    return records

# -----------------------------------
# Main pipeline
# -----------------------------------

def main():
    all_records = []

    for filename in os.listdir(FHIR_DIR):
        if filename.endswith(".json"):
            file_path = os.path.join(FHIR_DIR, filename)
            print(f"Processing {filename}")
            records = extract_observations(file_path)
            all_records.extend(records)

    df = pd.DataFrame(all_records)

    # Basic cleanup
    df = df.dropna(subset=["patient_id", "loinc_code", "value"])
    df = df.sort_values(["patient_id", "observation_date"])

    # Save output
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print("\n--- Biomarker extraction complete ---")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
