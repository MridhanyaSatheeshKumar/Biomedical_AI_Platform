CREATE TABLE patient_features AS
SELECT
    patient_id,

    MAX(CASE WHEN loinc_code='2339-0' THEN value END) AS glucose,
    MAX(CASE WHEN loinc_code='4548-4' THEN value END) AS hba1c,
    MAX(CASE WHEN loinc_code='2571-8' THEN value END) AS triglycerides,
    MAX(CASE WHEN loinc_code='38483-4' THEN value END) AS creatinine,
    MAX(CASE WHEN loinc_code='39156-5' THEN value END) AS bmi,
    MAX(CASE WHEN loinc_code='29463-7' THEN value END) AS weight

FROM observations
GROUP BY patient_id
ORDER BY patient_id;
