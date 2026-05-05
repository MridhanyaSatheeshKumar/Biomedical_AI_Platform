from neo4j import GraphDatabase
import pandas as pd
import os

print("\nBuilding FULL knowledge graph...\n")

# -----------------------------------
# Neo4j connection
# -----------------------------------

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "Mineo4jthu1@"))

# -----------------------------------
# Load FINAL dataset (important fix)
# -----------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

data_path = os.path.join(BASE_DIR, "data/semantic_ready/patient_dataset.csv")

df = pd.read_csv(data_path)

# -----------------------------------
# Graph creation
# -----------------------------------

def create_graph(tx, row):

    # Patient
    tx.run(
        "MERGE (p:Patient {id: $id})",
        id=row["patient_id"]
    )

    # BMI
    if pd.notna(row["bmi"]):
        tx.run(
            """
            MATCH (p:Patient {id: $id})
            MERGE (b:BMI {value: $val})
            MERGE (p)-[:HAS_BMI]->(b)
            """,
            id=row["patient_id"],
            val=float(row["bmi"])
        )

    # Glucose
    if pd.notna(row["glucose"]):
        tx.run(
            """
            MATCH (p:Patient {id: $id})
            MERGE (g:Glucose {value: $val})
            MERGE (p)-[:HAS_GLUCOSE]->(g)
            """,
            id=row["patient_id"],
            val=float(row["glucose"])
        )

    # Lifestyle
    if pd.notna(row["sleep_hours"]):
        tx.run(
            """
            MATCH (p:Patient {id: $id})
            MERGE (s:Sleep {hours: $val})
            MERGE (p)-[:HAS_SLEEP]->(s)
            """,
            id=row["patient_id"],
            val=float(row["sleep_hours"])
        )

    # Behavior
    if pd.notna(row["craving_frequency"]):
        tx.run(
            """
            MATCH (p:Patient {id: $id})
            MERGE (c:Craving {freq: $val})
            MERGE (p)-[:HAS_CRAVING]->(c)
            """,
            id=row["patient_id"],
            val=int(row["craving_frequency"])
        )

    # Condition (semantic part)
    if pd.notna(row["snomed_condition"]):
        tx.run(
            """
            MATCH (p:Patient {id: $id})
            MERGE (d:Disease {code: $code})
            MERGE (p)-[:AT_RISK_FOR]->(d)
            """,
            id=row["patient_id"],
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
