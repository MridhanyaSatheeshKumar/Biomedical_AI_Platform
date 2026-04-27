import pandas as pd

def load_data():
    df = pd.read_csv("data/food_logs.csv")
    return df

def preprocess(df):
    df = pd.get_dummies(df, columns=["time_of_day", "mood", "trigger", "food_type"])
    return df

if __name__ == "__main__":
    df = load_data()
    df = preprocess(df)
    print(df.head())
