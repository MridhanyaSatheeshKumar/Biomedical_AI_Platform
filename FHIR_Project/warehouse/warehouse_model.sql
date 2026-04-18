-- RAW LAYER
CREATE TABLE raw_observations AS
SELECT * FROM observations;


-- CLEAN LAYER
CREATE TABLE clean_observations AS
SELECT *
FROM raw_observations
WHERE value IS NOT NULL;


-- FEATURE LAYER (ANALYTICS READY)
CREATE TABLE analytics_patient_features AS
SELECT
    patient_id,
    MAX(CASE WHEN loinc_code='2339-0' THEN value END) AS glucose,
    MAX(CASE WHEN loinc_code='4548-4' THEN value END) AS hba1c,
    MAX(CASE WHEN loinc_code='2571-8' THEN value END) AS triglycerides,
    MAX(CASE WHEN loinc_code='38483-4' THEN value END) AS creatinine,
    MAX(CASE WHEN loinc_code='39156-5' THEN value END) AS bmi,
    MAX(CASE WHEN loinc_code='29463-7' THEN value END) AS weight
FROM clean_observations
GROUP BY patient_id;
