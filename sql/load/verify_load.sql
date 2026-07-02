-- Final Verification: Row Reconciliation
SET search_path TO production_medicare;

SELECT 'Patients' as table_name, COUNT(*) as row_count FROM patients
UNION ALL
SELECT 'Admissions', COUNT(*) FROM admissions
UNION ALL
SELECT 'Billing', COUNT(*) FROM billing
UNION ALL
SELECT 'Lab Results', COUNT(*) FROM lab_results;
