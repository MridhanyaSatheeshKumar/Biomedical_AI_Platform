# FHIR Semantic Clinical Data Engineering Pipeline for Glycemic Risk Modeling

This project implements a semantic clinical data engineering pipeline that integrates healthcare data from FHIR sources, harmonizes clinical observations using LOINC terminology, and generates machine-learning ready clinical feature tables for glycemic risk modeling.

The system demonstrates healthcare interoperability, semantic data normalization, biomedical ontology usage, and clinical feature engineering workflows commonly used in translational biomedical informatics research.

# Architecture Diagram


## Key Features

• FHIR clinical data ingestion (local and SMART FHIR sources)

• Ontology-driven biomarker extraction using LOINC codes

• Semantic clinical data harmonization into ML feature tables

• PostgreSQL clinical data warehouse integration

• Glycemic risk modeling using clinical biomarkers

• Modular biomedical data pipeline design

## Data Sources

The pipeline supports multiple clinical data ingestion pathways:

1 Synthetic FHIR data (Synthea bundles)

2 SMART FHIR clinical server integration

3 Structured clinical CSV ingestion (extensible)

This demonstrates integration of heterogeneous biomedical data sources.

## Technologies Used

Python
FHIR (Fast Healthcare Interoperability Resources)
LOINC biomedical terminology
PostgreSQL
SQL
scikit-learn
REST APIs
Healthcare data modeling
Neo4j
RDF
rdflib
SPARQL

## Pipeline Workflow

FHIR ingestion
→ Semantic normalization
→ Terminology filtering
→ Clinical feature harmonization
→ Machine learning modeling
→ Risk prediction output

### SPARQL Query Example

Query: Patients with BMI > 30

Result:
Patient_4d58... → BMI: 30.04
