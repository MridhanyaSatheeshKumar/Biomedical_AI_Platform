#!/bin/bash

echo "=============================="
echo "FHIR Semantic Data Platform"
echo "=============================="

# -------------------------------
# 1. Data Generation + Ingestion
# -------------------------------
echo "Step 1: Generating synthetic data..."
python3 data_pipeline/ingestion_layer/data_generation/generate_data.py

echo "Step 2: Ingesting FHIR data..."
python3 data_pipeline/ingestion_layer/ingestion/fhir_ingest.py


# -------------------------------
# 2. Database + Feature Extraction
# -------------------------------
echo "Step 3: Loading terminology mappings..."
sudo -u postgres psql -d fhir_db -f data_pipeline/analytics_layer/biomarker_extraction/loinc_terminology.sql
sudo -u postgres psql -d fhir_db -f data_pipeline/analytics_layer/biomarker_extraction/snomed_conditions.sql

echo "Step 4: Extracting biomarkers..."
sudo -u postgres psql -d fhir_db -f data_pipeline/analytics_layer/biomarker_extraction/metabolic_biomarkers.sql

echo "Step 5: Exporting feature table..."
sudo -u postgres psql -d fhir_db -c "\COPY patient_features TO 'data/patient_features.csv' CSV HEADER"


# -------------------------------
# 3. Data Processing + Validation
# -------------------------------
echo "Step 6: Building integrated patient profile..."
python3 data_pipeline/processing_layer/Integration/build_patient_profile.py

echo "Step 7: Running data quality checks..."
python3 data_pipeline/processing_layer/validation/data_quality_checks.py

echo "Step 8: Spark processing..."
python3 data_pipeline/processing_layer/spark/spark_processing.py


# -------------------------------
# 4. Semantic Layer
# -------------------------------
echo "Step 9: Building knowledge graph (Neo4j)..."
python3 semantic_layer/knowledge_graph/build_full_knowledge_graph.py

echo "Step 10: Exporting RDF..."
python3 semantic_layer/semantic_rdf/export_rdf.py

echo "Step 11: Loading ontology instances..."
python3 semantic_layer/ontology_model/load_ontology_instances.py

echo "Step 12: Mapping ontology conditions..."
python3 semantic_layer/ontology_model/map_conditions.py

echo "Step 13: Running reasoning..."
python3 semantic_layer/inference/clinical_reasoning.py


# -------------------------------
# 5. ML Layer
# -------------------------------
echo "Step 14: Running ML model..."
python3 data_pipeline/analytics_layer/modeling/glycemic_risk_model.py

echo "Step 15: Running health insights application..."
python3 application/health_insights_app/main.py

echo "=============================="
echo "Pipeline completed successfully!"
echo "=============================="
