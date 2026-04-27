SELECT
    o.patient_id,
    o.loinc_code,
    t.concept_name,
    t.category,
    o.value,
    o.unit,
    o.observation_date

FROM observations o

JOIN loinc_terminology t
ON o.loinc_code = t.loinc_code

ORDER BY o.patient_id,o.observation_date;
