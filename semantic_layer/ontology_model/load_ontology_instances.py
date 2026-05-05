from rdflib import Graph, Namespace, Literal, RDF, URIRef
import pandas as pd
import os

print("\n--- Loading ontology instances ---\n")

# -----------------------------------
# Setup paths
# -----------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
data_path = os.path.join(BASE_DIR, "data/semantic_ready/patient_dataset.csv")

df = pd.read_csv(data_path)

# -----------------------------------
# RDF setup
# -----------------------------------

EX = Namespace("http://example.org/health/")

g = Graph()
g.bind("ex", EX)

# -----------------------------------
# Create instances
# -----------------------------------

for _, row in df.iterrows():

    patient_id = str(row["patient_id"])
    patient = URIRef(EX[f"Patient_{patient_id}"])

    g.add((patient, RDF.type, EX.Patient))

    # BMI
    if pd.notna(row.get("bmi")):
        bmi = URIRef(EX[f"BMI_{patient_id}"])
        g.add((bmi, RDF.type, EX.BMI))
        g.add((bmi, EX.hasValue, Literal(float(row["bmi"]))))
        g.add((patient, EX.hasBiomarker, bmi))

    # Glucose
    if pd.notna(row.get("glucose")):
        glucose = URIRef(EX[f"Glucose_{patient_id}"])
        g.add((glucose, RDF.type, EX.Glucose))
        g.add((glucose, EX.hasValue, Literal(float(row["glucose"]))))
        g.add((patient, EX.hasBiomarker, glucose))

# -----------------------------------
# Save RDF
# -----------------------------------

output_path = os.path.join(BASE_DIR, "semantic_layer/ontology_model/ontology_instances.ttl")
g.serialize(output_path, format="turtle")

print(f"Ontology instances saved to: {output_path}")
