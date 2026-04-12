import pandas as pd

df = pd.read_csv("data/patient_features.csv")

print("\nRunning clinical reasoning rules...\n")

df["glycemic_risk_rule"] = 0

df["obesity_risk"] = 0

df["lipid_risk"] = 0


# Rule 1 — Diabetes risk

df.loc[df["hba1c"] > 6.5, "glycemic_risk_rule"] = 1

df.loc[df["glucose"] > 126, "glycemic_risk_rule"] = 1


# Rule 2 — Obesity risk

df.loc[df["bmi"] > 30, "obesity_risk"] = 1


# Rule 3 — Lipid risk

df.loc[df["triglycerides"] > 200, "lipid_risk"] = 1


print("Risk counts:")

print("Glycemic risk:", df["glycemic_risk_rule"].sum())

print("Obesity risk:", df["obesity_risk"].sum())

print("Lipid risk:", df["lipid_risk"].sum())


df.to_csv(
    "data/patient_features_with_rules.csv",
    index=False
)

print("\nClinical reasoning complete")
print("Output saved")
