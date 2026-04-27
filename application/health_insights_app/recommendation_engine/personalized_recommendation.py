import pandas as pd
import os

print("\nGenerating personalized recommendations...\n")

# Load integrated data
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

data_path = os.path.join(
    BASE_DIR,
    "Integration/patient_integrated_profile.csv"
)

df = pd.read_csv(data_path)


def generate_recommendation(row):

    recommendations = []

    # Glycemic risk
    if row.get("glycemic_risk_rule", 0) == 1:
        recommendations.append("Reduce sugar intake")

    # BMI
    if "bmi_x" in row and pd.notna(row["bmi_x"]) and row["bmi_x"] > 30:
        recommendations.append("Adopt calorie deficit diet")

    # Sleep
    if "sleep_hours" in row and pd.notna(row["sleep_hours"]) and row["sleep_hours"] < 6:
        recommendations.append("Improve sleep duration")

    # Cravings
    if "craving_frequency" in row and pd.notna(row["craving_frequency"]) and row["craving_frequency"] > 5:
        recommendations.append("Reduce processed food consumption")

    if not recommendations:
        recommendations.append("Maintain healthy lifestyle")

    return "; ".join(recommendations)


# Apply recommendations
df["recommendation"] = df.apply(generate_recommendation, axis=1)

# Save output
output_path = os.path.join(
    BASE_DIR,
    "Personalized_Nutrition_AI/data/personalized_recommendations.csv"
)

df.to_csv(output_path, index=False)

print("Recommendations generated successfully")
print(f"Saved to: {output_path}")
