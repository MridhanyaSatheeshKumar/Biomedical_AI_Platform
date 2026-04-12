# Metabolic Biomarker Dataset

This dataset is generated from the FHIR clinical observations table.

Source:
FHIR synthetic EHR data generated using Synthea.

Extraction:
The dataset is created using the SQL query:

biomarker_extraction/metabolic_biomarkers.sql

Export command used in PostgreSQL:

COPY (
    SELECT
        patient_id,
        loinc_code,
        test_name,
        value,
        unit,
        observation_date
    FROM observations
    WHERE loinc_code IN (
        '2339-0','4548-4','2571-8','38483-4',
        '6299-2','2947-0','6298-4','39156-5','29463-7'
    )
) TO '/tmp/metabolic_biomarkers.csv'
WITH CSV HEADER;

Purpose:
Dataset used for predictive modeling of glycemic risk.
