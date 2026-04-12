from neo4j import GraphDatabase
import pandas as pd
import os

print("\nAdding LOINC → SNOMED links...\n")

# Neo4j connection
uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))

# Load mapping file
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

mapping_path = os.path.join(
    BASE_DIR,
    "biomarker_extraction/loinc_snomed_mapping.csv"
)

df = pd.read_csv(mapping_path)


def create_links(tx, row):

    tx.run(
        """
        MERGE (l:Biomarker {name: $name})
        MERGE (d:Disease {code: $code, name: $disease})
        MERGE (l)-[:INDICATES]->(d)
        """,
        name=row["concept_name"],
        code=row["snomed_code"],
        disease=row["disease_name"]
    )


with driver.session() as session:
    for _, row in df.iterrows():
        session.execute_write(create_links, row)

driver.close()

print("LOINC → SNOMED links added")
