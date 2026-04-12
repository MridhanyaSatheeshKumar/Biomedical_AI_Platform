from rdflib import Graph

print("\nRunning SPARQL queries...\n")

g = Graph()

# Load RDF (Turtle format)
g.parse("data/patient_features.rdf", format="turtle")

# Query: Patients with BMI > 30
query = """
SELECT ?patient ?bmi
WHERE {
    ?patient <http://example.org/health/hasBMI> ?bmi .
    FILTER (?bmi > 30)
}
"""

results = g.query(query)

found = False

for row in results:
    found = True
    print(f"Patient: {row.patient}, BMI: {row.bmi}")

if not found:
    print("No patients found with BMI > 30")
