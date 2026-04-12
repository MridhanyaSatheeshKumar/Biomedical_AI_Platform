from neo4j import GraphDatabase
import pandas as pd
import os

print("\nBuilding FULL knowledge graph...\n")

# -----------------------------------
# Neo4j connection
# -----------------------------------

uri = "bolt://localhost:7687"
user = "neo4j"
password = "password"

driver = GraphDatabase.driver(uri, auth=(user, password))


# -----------------------------------
# Load integrated dataset
# -----------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

data_path = os.path.join(
    BASE_DIR,
    "Integration/patient_integrated_profile.csv"
)

df = pd.read_csv(data_path)

# Normalize column names
df.columns = df.columns.str.lower()

# Fix merged column names
if "bmi_x" in df.columns:
    df.rename(columns={"bmi_x": "bmi"}, inplace=True)

if "glucose_x" in df.columns:
    df.rename(columns={"glucose_x": "glucose"}, inplace=True)

# -----------------------------------
# Graph creation logic
# -----------------------------------

def create_graph(tx, row):

    # Patient node
    tx.run(
        """
        MERGE (p:Patient {id: $patient_id})
        """,
        patient_id=row["patient_id"]
    )

    # -----------------------------
    # BMI
    # -----------------------------
    if pd.notna(row["bmi"]):
        tx.run(
            """
            MATCH (p:Patient {id: $patient_id})
            MERGE (b:BMI {value: $bmi})
            MERGE (p)-[:HAS_BMI]->(b)
            """,
            patient_id=row["patient_id"],
            bmi=float(row["bmi"])
        )

    # -----------------------------
    # Glucose
    # -----------------------------
    if pd.notna(row["glucose"]):
        tx.run(
            """
            MATCH (p:Patient {id: $patient_id})
            MERGE (g:Glucose {value: $glucose})
            MERGE (p)-[:HAS_GLUCOSE]->(g)
            """,
            patient_id=row["patient_id"],
            glucose=float(row["glucose"])
        )

    # -----------------------------
    # Food craving
    # -----------------------------
    if pd.notna(row["craving_frequency"]):
        tx.run(
            """
            MATCH (p:Patient {id: $patient_id})
            MERGE (c:Craving {frequency: $freq})
            MERGE (p)-[:HAS_CRAVING]->(c)
            """,
            patient_id=row["patient_id"],
            freq=int(row["craving_frequency"])
        )

    # -----------------------------
    # Sleep
    # -----------------------------
    if pd.notna(row["sleep_hours"]):
        tx.run(
            """
            MATCH (p:Patient {id: $patient_id})
            MERGE (s:Sleep {hours: $sleep})
            MERGE (p)-[:HAS_SLEEP]->(s)
            """,
            patient_id=row["patient_id"],
            sleep=float(row["sleep_hours"])
        )

    # -----------------------------
    # SNOMED condition
    # -----------------------------
    if pd.notna(row["snomed_condition"]):
        tx.run(
            """
            MATCH (p:Patient {id: $patient_id})
            MERGE (d:Disease {code: $code})
            MERGE (p)-[:AT_RISK_FOR]->(d)
            """,
            patient_id=row["patient_id"],
            code=row["snomed_condition"]
        )


# -----------------------------------
# Run graph build
# -----------------------------------

with driver.session() as session:
    for _, row in df.iterrows():
        session.execute_write(create_graph, row)

driver.close()

print("Full knowledge graph created successfully")
