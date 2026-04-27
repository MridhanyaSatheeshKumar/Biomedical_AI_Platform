                 DATA SOURCES
 ┌─────────────────────────────────────────────┐
 │                                             │
 │  Synthetic FHIR Data (Synthea)              │
 │  SMART FHIR API (Clinical Server)           │
 │  Structured Health CSV Data                 │
 │                                             │
 └─────────────────────────────────────────────┘
                      │
                      ▼ 

              DATA INGESTION LAYER
 ┌─────────────────────────────────────────────┐
 │ ingestion/fhir_ingest.py                    │
 │ ingestion/smart_secure_client.py            │
 │                                             │
 │ Functions:                                  │
 │ • FHIR bundle upload                        │
 │ • SMART API extraction                      │
 │ • Clinical resource parsing                 │
 │                                             │
 └─────────────────────────────────────────────┘
                      │
                      ▼

            SEMANTIC NORMALIZATION LAYER
 ┌─────────────────────────────────────────────┐
 │ PostgreSQL FHIR database                    │
 │                                             │
 │ Functions:                                  │
 │ • Standardized patient schema               │
 │ • Observation normalization                 │
 │ • Terminology alignment (LOINC codes)       │
 │                                             │
 └─────────────────────────────────────────────┘
                      │
                      ▼

         SEMANTIC FEATURE ENGINEERING LAYER
 ┌─────────────────────────────────────────────┐
 │ metabolic_biomarkers.sql                    │
 │ patient_feature_table.sql                   │
 │                                             │
 │ Functions:                                  │
 │ • Biomarker extraction                      │
 │ • Ontology-driven filtering                 │
 │ • Clinical feature construction             │
 │ • Data harmonization                        │
 │                                             │
 └─────────────────────────────────────────────┘
                      │
                      ▼

               MACHINE LEARNING LAYER
 ┌─────────────────────────────────────────────┐
 │ glycemic_risk_model.py                      │
 │                                             │
 │ Functions:                                  │
 │ • Clinical risk labeling                    │
 │ • Feature preprocessing                     │
 │ • Risk prediction modeling                  │
 │                                             │
 └─────────────────────────────────────────────┘
                      │
                      ▼

                ANALYTICS OUTPUT
 ┌─────────────────────────────────────────────┐
 │ patient_features.csv                        │
 │ glycemic_risk_model.pkl                     │
 │                                             │
 │ Outputs:                                    │
 │ • Clinical feature tables                   │
 │ • Risk scores                               │
 │ • ML-ready datasets                         │
 │                                             │
 └─────────────────────────────────────────────┘


# Pipeline Architecture

## Data Sources

Synthetic FHIR bundles  
SMART FHIR server  
Structured clinical datasets  

## Data Ingestion Layer

Scripts:

ingestion/fhir_ingest.py  
ingestion/smart_secure_client.py  

Purpose:

FHIR resource ingestion  
API extraction  
Clinical data parsing  

## Semantic Normalization Layer

PostgreSQL clinical database.

Purpose:

FHIR resource normalization  
Terminology alignment  
Observation storage  

## Feature Engineering Layer

SQL scripts:

metabolic_biomarkers.sql  
patient_feature_table.sql  

Purpose:

Clinical biomarker extraction  
Feature construction  
Data harmonization  

## ML Layer

glycemic_risk_model.py

Purpose:

Risk labeling  
Feature preprocessing  
Model training  

## Outputs

patient_features.csv  
glycemic_risk_model.pkl


