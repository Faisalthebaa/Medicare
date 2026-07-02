-- Step 3: Create Patient Risk Profile View
SET search_path TO production_medicare;

CREATE OR REPLACE VIEW v_patient_risk_profile AS
SELECT 
    l.lab_id,
    p.patient_id,
    p.first_name || ' ' || p.last_name as patient_name,
    p.comorbidity_score,
    l.test_name,
    l.result_value,
    l.flag as clinical_flag,
    a.department,
    a.outcome,
    a.readmitted_30d
FROM lab_results l
JOIN patients p ON l.patient_id = p.patient_id
JOIN admissions a ON l.admission_id = a.admission_id
WHERE l.flag = 'High';
