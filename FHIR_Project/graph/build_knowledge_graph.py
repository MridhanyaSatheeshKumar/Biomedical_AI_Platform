from neo4j import GraphDatabase
import pandas as pd

URI = "bolt://localhost:7687"

USER = "neo4j"

PASSWORD = "password"   # change if you used different password


driver = GraphDatabase.driver(
    URI,
    auth=(USER, PASSWORD)
)


df = pd.read_csv("data/patient_features.csv")

df = df.fillna(0)

df = df.replace({None: pd.NA})

def create_patient_graph(tx,row):

    tx.run(

        """
        MERGE (p:Patient {id:$id})
        """,

        id=row["patient_id"]

    )


    if pd.notna(row.get("bmi")):

        tx.run(

        """

        MERGE (b:BMI {value:$bmi})

        MERGE (p:Patient {id:$id})

        MERGE (p)-[:HAS_BMI]->(b)

        """,

        id=row["patient_id"],

        bmi=float(row["bmi"])

        )


    if pd.notna(row.get("triglycerides")):

        tx.run(

        """

        MERGE (t:Triglycerides {value:$trig})

        MERGE (p:Patient {id:$id})

        MERGE (p)-[:HAS_TRIGLYCERIDES]->(t)

        """,

        id=row["patient_id"],

        trig=float(row["triglycerides"])

        )


    if pd.notna(row.get("creatinine")):

        tx.run(

        """

        MERGE (c:Creatinine {value:$creat})

        MERGE (p:Patient {id:$id})

        MERGE (p)-[:HAS_CREATININE]->(c)

        """,

        id=row["patient_id"],

        creat=float(row["creatinine"])

        )

with driver.session() as session:

    for _,row in df.iterrows():

        session.execute_write(
            create_patient_graph,row
        )


print("Knowledge graph created successfully")
