import pandas as pd
import random
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
RAW_PATH = os.path.join(BASE_DIR, "data", "raw")

os.makedirs(RAW_PATH, exist_ok=True)

# -------------------------
# Load clinical IDs
# -------------------------

clinical_path = os.path.join(BASE_DIR, "data", "processed", "patient_features_semantic.csv")

clinical = pd.read_csv(clinical_path)

users = clinical["patient_id"].tolist()

# -------------------------
# Generate Food Logs
# -------------------------

times = ["morning", "afternoon", "evening", "night"]
moods = ["stress", "happy", "bored", "neutral"]
triggers = ["work", "home", "social", "hunger"]
foods = ["chocolate", "chips", "fast_food", "ice_cream", "fruit"]

food_data = []

for _ in range(300):

    user = random.choice(users)

    food_data.append({

        "patient_id": user,
        "time_of_day": random.choice(times),
        "mood": random.choice(moods),
        "trigger": random.choice(triggers),
        "food_type": random.choice(foods),
        "calories": random.randint(100, 600)

    })

food_df = pd.DataFrame(food_data)

food_df.to_csv(
    os.path.join(RAW_PATH, "food_logs.csv"),
    index=False
)

print("Food logs generated")


# -------------------------
# Generate Health Data
# -------------------------

health_data = []

for user in users:

    health_data.append({

        "patient_id": user,
        "glucose": random.randint(80, 180),
        "hba1c": round(random.uniform(4.5, 8.5), 1),
        "bmi": random.randint(18, 35),
        "stress_level": random.randint(1, 10),
        "sleep_hours": random.randint(4, 9),
        "craving_level": random.randint(1, 10),
        "risk_flag": random.randint(0, 1)

    })

health_df = pd.DataFrame(health_data)

health_df.to_csv(
    os.path.join(RAW_PATH, "user_health_data.csv"),
    index=False
)

print("Health data generated")
