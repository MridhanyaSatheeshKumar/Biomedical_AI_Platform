# Pipeline Architecture

---

## Overview

This pipeline processes heterogeneous healthcare data and transforms it into a unified, semantically enriched patient dataset suitable for analysis, knowledge graph construction, and clinical reasoning.

The architecture is designed to be modular, extensible, and aligned with real-world biomedical data workflows.

---

## End-to-End Flow


FHIR + Behavioral + Lifestyle Data
↓
Biomarker Extraction (LOINC normalization)
↓
Patient Feature Engineering
↓
Data Cleaning & Validation
↓
Data Integration (Unified Patient Dataset)
↓
Semantic Transformation (RDF)
↓
Ontology Mapping
↓
Knowledge Graph (Neo4j)
↓
Clinical Reasoning


---

## Pipeline Layers

---

### 1. Data Sources

- Synthetic clinical data (FHIR bundles from Synthea)
- Behavioral data (food logs)
- Lifestyle data (health metrics)

These represent heterogeneous healthcare data sources commonly found in real systems.

---

### 2. Ingestion Layer *(Further Expansion)*

**Location:**
- `data_pipeline/ingestion/`

**Purpose:**
- Handles FHIR data ingestion
- Designed for real-world integration with external systems

> Note: In the current pipeline, local FHIR bundles are directly processed for reproducibility.

---

### 3. Transformation Layer

#### Biomarker Extraction

**File:**
- `extract_biomarkers.py`

**Function:**
- Parses FHIR Observation resources
- Filters LOINC-coded lab measurements
- Produces structured biomarker dataset

---

#### Feature Engineering

**File:**
- `build_patient_features.py`

**Function:**
- Aggregates biomarker data at patient level
- Applies clinical rules (e.g., glucose, HbA1c thresholds)
- Maps inferred risks to SNOMED conditions
- Produces patient feature table

---

### 4. Validation Layer

**Files:**
- `pre_clean.py`
- `data_quality_checks.py`

**Function:**
- Cleans and normalizes datasets
- Handles missing values and duplicates
- Performs basic data quality validation

---

### 5. Integration Layer

**File:**
- `build_patient_profile.py`

**Function:**
- Merges clinical, behavioral, and lifestyle datasets
- Resolves feature conflicts across sources
- Applies selective missing value handling
- Produces unified patient dataset

**Output:**

data/semantic_ready/patient_dataset.csv


---

### 6. Semantic Layer

**Location:**
- `semantic_layer/`

**Function:**
- Converts structured data into RDF triples
- Aligns data with ontology concepts
- Enables semantic querying and reasoning

---

### 7. Knowledge Graph Layer

**Tool:**
- Neo4j

**Function:**
- Represents patients, biomarkers, and risks as graph nodes
- Captures relationships between entities
- Enables graph-based queries

---

### 8. Inference Layer

**File:**
- `clinical_reasoning.py`

**Function:**
- Applies rule-based clinical logic
- Infers patient risk categories
- Adds inferred relationships to the graph

---

## Key Design Principles

- Modular pipeline architecture
- Clear separation of concerns
- Semantic enrichment over raw data processing
- Realistic handling of incomplete healthcare data
- Extensibility to real-world systems
