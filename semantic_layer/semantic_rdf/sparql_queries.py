from rdflib import Graph
import os

print("\n--- Running SPARQL queries ---\n")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
rdf_path = os.path.join(BASE_DIR, "data/patient_features.rdf")

g = Graph()
g.parse(rdf_path, format="turtle")

query = """
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?patient ?bmi
WHERE {
    ?patient <http://example.org/health/hasBMI> ?bmi .
    FILTER (xsd:float(?bmi) > 30)
}
"""

results = g.query(query)

found = False

for row in results:
    found = True
    print(f"Patient: {row.patient}, BMI: {row.bmi}")

if not found:
    print("No patients found with BMI > 30")
