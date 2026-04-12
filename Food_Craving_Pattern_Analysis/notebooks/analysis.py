import pandas as pd

df = pd.read_csv("data/food_logs.csv")

print(df.groupby("mood")["calories"].mean())
print(df.groupby("time_of_day")["calories"].mean())
