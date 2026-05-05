from neo4j import GraphDatabase
import pandas as pd
import os

print("\nRunning clinical reasoning...\n")

# -----------------------------------
# Load FINAL dataset
# -----------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
data_path = os.path.join(BASE_DIR, "data/semantic_ready/patient_dataset.csv")

df = pd.read_csv(data_path)

# -----------------------------------
# Apply reasoning rules
# -----------------------------------

df["glycemic_risk"] = 0
df["obesity_risk"] = 0
df["lipid_risk"] = 0

# Glycemic risk
df.loc[(df["hba1c"] > 6.5) | (df["glucose"] > 126), "glycemic_risk"] = 1

# Obesity risk
df.loc[df["bmi"] > 30, "obesity_risk"] = 1

# Lipid risk
df.loc[df["triglycerides"] > 200, "lipid_risk"] = 1

print("Risk summary:")
print(df[["glycemic_risk","obesity_risk","lipid_risk"]].sum())

# -----------------------------------
# Neo4j connection
# -----------------------------------

driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "Mineo4jthu1@")
)

# -----------------------------------
# Push reasoning into graph
# -----------------------------------

def add_risk(tx, row):

    if row["glycemic_risk"] == 1:
        tx.run("""
            MATCH (p:Patient {id: $id})
            MERGE (r:Risk {type: "Glycemic"})
            MERGE (p)-[:HAS_RISK]->(r)
        """, id=row["patient_id"])

    if row["obesity_risk"] == 1:
        tx.run("""
            MATCH (p:Patient {id: $id})
            MERGE (r:Risk {type: "Obesity"})
            MERGE (p)-[:HAS_RISK]->(r)
        """, id=row["patient_id"])

    if row["lipid_risk"] == 1:
        tx.run("""
            MATCH (p:Patient {id: $id})
            MERGE (r:Risk {type: "Lipid"})
            MERGE (p)-[:HAS_RISK]->(r)
        """, id=row["patient_id"])

# -----------------------------------
# Execute
# -----------------------------------

with driver.session() as session:
    for _, row in df.iterrows():
        session.execute_write(add_risk, row)

driver.close()

print("\nClinical reasoning added to graph")
