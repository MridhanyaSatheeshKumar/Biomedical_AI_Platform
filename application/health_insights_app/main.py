import pandas as pd

print("Running Health Insights Application...")

# Load processed data
df = pd.read_csv("../../data/patient_features_with_rules.csv")

# Example logic
high_risk = df[df["risk_flag"] == 1]

print(f"High-risk patients: {len(high_risk)}")

# Placeholder for recommendation engine
print("Generating personalized recommendations...")
