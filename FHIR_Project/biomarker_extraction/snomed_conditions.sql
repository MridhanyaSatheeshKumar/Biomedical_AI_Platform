CREATE TABLE snomed_conditions (

condition_name TEXT,

snomed_code TEXT PRIMARY KEY,

category TEXT

);


INSERT INTO snomed_conditions VALUES

('Diabetes Mellitus','44054006','Metabolic disorder'),

('Obesity','414916001','Metabolic disorder'),

('Hyperlipidemia','55822004','Lipid disorder');
