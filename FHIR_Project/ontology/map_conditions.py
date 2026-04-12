import pandas as pd

df = pd.read_csv("data/patient_features_with_rules.csv")

print("\nMapping risks to SNOMED conditions...\n")


df["snomed_condition"] = None


df.loc[
    df["glycemic_risk_rule"] == 1,
    "snomed_condition"
] = "44054006"


df.loc[
    df["obesity_risk"] == 1,
    "snomed_condition"
] = "414916001"


df.loc[
    df["lipid_risk"] == 1,
    "snomed_condition"
] = "55822004"


df.to_csv(
    "data/patient_features_semantic.csv",
    index=False
)


print("SNOMED mapping complete")
