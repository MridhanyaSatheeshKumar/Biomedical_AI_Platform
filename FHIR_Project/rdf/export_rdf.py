import pandas as pd

from rdflib import Graph, Literal, Namespace, URIRef


df = pd.read_csv("data/patient_features.csv")


g = Graph()


# Define namespace

EX = Namespace("http://example.org/health/")


for _,row in df.iterrows():

    patient = URIRef(EX + "Patient_" + str(row["patient_id"]))

    if pd.notna(row.get("bmi")):

        g.add(
            (
                patient,
                EX.hasBMI,
                Literal(row["bmi"])
            )
        )


    if pd.notna(row.get("triglycerides")):

        g.add(
            (
                patient,
                EX.hasTriglycerides,
                Literal(row["triglycerides"])
            )
        )


    if pd.notna(row.get("creatinine")):

        g.add(
            (
                patient,
                EX.hasCreatinine,
                Literal(row["creatinine"])
            )
        )


g.serialize(
    "data/patient_features.rdf",
    format="turtle"
)


print("RDF triples exported")
