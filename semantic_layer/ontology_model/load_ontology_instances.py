from rdflib import Graph, Namespace, Literal, RDF, URIRef

# Load namespace
EX = Namespace("http://example.org/health/")

g = Graph()

# Load CSV
import pandas as pd
df = pd.read_csv("../../Integration/patient_integrated_profile.csv")

for _, row in df.iterrows():
    patient_id = str(row["patient_id"])

    patient = URIRef(EX[f"Patient_{patient_id}"])
    g.add((patient, RDF.type, EX.Patient))

    # BMI
    if pd.notna(row["bmi_y"]):
        bmi = URIRef(EX[f"BMI_{patient_id}"])
        g.add((bmi, RDF.type, EX.BMI))
        g.add((bmi, EX.hasValue, Literal(float(row["bmi_y"]))))

        g.add((patient, EX.hasBiomarker, bmi))

# Save RDF
g.serialize("ontology_instances.ttl", format="turtle")

print("Ontology instances created")
