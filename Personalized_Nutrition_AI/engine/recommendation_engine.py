import pandas as pd

df = pd.read_csv("data/user_health_data.csv")

def generate_recommendation(row):
    recommendations = []

    # Clinical risk
    if row["hba1c"] >= 6.5:
        recommendations.append("⚠️ High diabetes risk: reduce sugar, monitor glucose")

    if row["glucose"] > 130:
        recommendations.append("Avoid high glycemic foods")

    if row["bmi"] > 25:
        recommendations.append("Increase physical activity and calorie control")

    # Behavioral risk
    if row["stress_level"] > 7:
        recommendations.append("High stress: consider mindfulness / stress control")

    if row["sleep_hours"] < 6:
        recommendations.append("Improve sleep (target 7–8 hours)")

    if row["binge_risk"] == 1:
        recommendations.append("🚨 High binge risk: avoid trigger foods tonight")

    return " | ".join(recommendations)

df["recommendations"] = df.apply(generate_recommendation, axis=1)

print(df[["user_id", "recommendations"]])
