import pandas as pd
from rdflib import Graph, Literal, Namespace, URIRef, XSD
import os

print("\n--- Exporting RDF ---\n")

# -----------------------------------
# Setup paths
# -----------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
data_path = os.path.join(BASE_DIR, "data/semantic_ready/patient_dataset.csv")

df = pd.read_csv(data_path)

# -----------------------------------
# RDF setup
# -----------------------------------

g = Graph()
EX = Namespace("http://example.org/health/")
g.bind("ex", EX)

# -----------------------------------
# Helper function (IMPORTANT FIX)
# -----------------------------------

def clean_float(value):
    """Convert to float, round, and attach datatype"""
    return Literal(round(float(value), 2), datatype=XSD.float)

# -----------------------------------
# Build RDF triples
# -----------------------------------

for _, row in df.iterrows():

    patient = URIRef(EX[f"Patient_{row['patient_id']}"])

    # BMI
    if pd.notna(row.get("bmi")):
        g.add((patient, EX.hasBMI, clean_float(row["bmi"])))

    # Triglycerides
    if pd.notna(row.get("triglycerides")):
        g.add((patient, EX.hasTriglycerides, clean_float(row["triglycerides"])))

    # Creatinine
    if pd.notna(row.get("creatinine")):
        g.add((patient, EX.hasCreatinine, clean_float(row["creatinine"])))

# -----------------------------------
# Save RDF
# -----------------------------------

output_path = os.path.join(BASE_DIR, "data/patient_features.rdf")
g.serialize(output_path, format="turtle")

print(f"RDF saved to: {output_path}")
