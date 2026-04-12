#!/bin/bash

echo "Starting FHIR ingestion..."

python3 ingestion/fhir_ingest.py

echo "Loading terminology mapping..."

sudo -u postgres psql -d fhir_db -f biomarker_extraction/loinc_terminology.sql

echo "Extracting biomarkers..."

sudo -u postgres psql -d fhir_db -f biomarker_extraction/metabolic_biomarkers.sql

echo "Exporting feature table..."

sudo -u postgres psql -d fhir_db -c "\COPY patient_features TO 'data/patient_features.csv' CSV HEADER"

echo "Running data quality validation..."

python3 validation/data_quality_checks.py

echo "Building knowledge graph..."

python3 graph/build_knowledge_graph.py

echo "Exporting RDF triples..."

python3 rdf/export_rdf.py

echo "Running clinical reasoning..."

python3 reasoning/clinical_reasoning.py

echo "Mapping clinical ontology..."

python3 ontology/map_conditions.py

echo "Running ML model..."

python3 modeling/glycemic_risk_model.py

echo "Pipeline complete."
