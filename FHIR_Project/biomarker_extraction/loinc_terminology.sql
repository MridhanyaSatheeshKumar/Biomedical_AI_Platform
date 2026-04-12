CREATE TABLE loinc_terminology (

    loinc_code VARCHAR PRIMARY KEY,

    concept_name TEXT,

    category TEXT,

    clinical_use TEXT

);


INSERT INTO loinc_terminology VALUES

('2339-0','Glucose','Metabolic Panel','Diabetes risk biomarker'),

('4548-4','HbA1c','Diabetes Panel','Long term glucose control'),

('2571-8','Triglycerides','Lipid Panel','Cardiometabolic risk'),

('38483-4','Creatinine','Renal Panel','Kidney function'),

('6299-2','Urea Nitrogen','Renal Panel','Kidney function'),

('2947-0','Sodium','Electrolyte Panel','Fluid balance'),

('6298-4','Potassium','Electrolyte Panel','Electrolyte balance'),

('39156-5','BMI','Vitals','Obesity indicator'),

('29463-7','Body Weight','Vitals','Body mass measurement');
