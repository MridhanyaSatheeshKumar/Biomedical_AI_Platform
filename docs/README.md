# Biomedical AI Semantic Data Platform

This project implements an end-to-end biomedical data engineering pipeline that transforms raw healthcare data into a semantically enriched knowledge system for analysis and clinical reasoning.

---

## Overview

The system integrates heterogeneous healthcare data sources — including clinical (FHIR), behavioral, and lifestyle data — into a unified patient-level dataset, and extends it into a semantic layer using RDF, ontology modeling, and graph-based reasoning.

---

## Key Capabilities

- FHIR-based clinical data processing (Synthea)
- LOINC-driven biomarker extraction and normalization
- Patient-level feature engineering with clinical rules
- Multi-source data integration (clinical + behavioral + lifestyle)
- RDF generation for semantic interoperability
- Ontology alignment using LOINC and SNOMED
- Knowledge graph construction using Neo4j
- Rule-based clinical reasoning (risk inference)

---

## System Architecture


FHIR + CSV Data
↓
Biomarker Extraction (LOINC)
↓
Patient Feature Engineering
↓
Data Cleaning & Validation
↓
Data Integration (Unified Patient Dataset)
↓
RDF Transformation
↓
Ontology Mapping
↓
Knowledge Graph (Neo4j)
↓
Clinical Reasoning


---

## Core Components

### 1. Data Pipeline
- Processes FHIR clinical observations
- Extracts key metabolic biomarkers
- Builds patient-level feature tables
- Cleans and validates datasets
- Integrates multiple data sources into a unified dataset

---

### 2. Ontology Layer
- Uses **LOINC** for lab test standardization
- Uses **SNOMED CT** for disease/condition representation
- Maintains mappings between biomarkers and clinical conditions

---

### 3. Semantic Layer
- Converts structured data into RDF triples
- Aligns data with ontology concepts
- Enables querying (SPARQL) and graph-based analysis
- Supports rule-based reasoning for clinical insights

---

## Data Flow


Raw Data (FHIR + Behavioral + Lifestyle)
↓
Biomarker Extraction (LOINC normalization)
↓
Feature Engineering (patient-level)
↓
Data Cleaning & Validation
↓
Integration (unified patient dataset)
↓
Semantic Layer (RDF → Ontology → Graph → Reasoning)


---

## Purpose

This system demonstrates how real-world healthcare data can be:

- standardized using clinical terminologies
- transformed into meaningful patient-level features
- integrated across multiple domains
- represented as a knowledge graph
- used for explainable clinical reasoning

---

## Design Philosophy

- Modular pipeline architecture
- Separation of data, semantic, and reasoning layers
- Realistic handling of incomplete healthcare data
- Focus on semantic enrichment over raw modeling

---

## How to Run

```bash
python run_pipeline.py
```
---

## Outputs
data/semantic_ready/patient_dataset.csv → integrated dataset
data/patient_features.rdf → RDF triples
Neo4j graph → patient relationships and inferred risks
