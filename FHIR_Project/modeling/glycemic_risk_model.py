import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# load dataset
df = pd.read_csv("data/patient_features.csv")

print("Dataset shape:", df.shape)
print(df.head())

# fill missing values with the mean
df = df.fillna(df.mean(numeric_only=True))

# create risk label
df["glycemic_risk"] = (df["glucose"] > df["glucose"].median()).astype(int)
print(df["glycemic_risk"].value_counts())

X = df[["bmi","triglycerides","creatinine","weight"]]
y = df["glycemic_risk"]

X_train, X_test, y_train, y_test = train_test_split(
    X,y,test_size=0.2,random_state=42
)

model = LogisticRegression(class_weight="balanced")

model.fit(X_train,y_train)

preds = model.predict(X_test)

print(classification_report(y_test,preds))


import joblib

joblib.dump(model, "modeling/glycemic_risk_model.pkl")

print("Model saved to modeling/glycemic_risk_model.pkl")
