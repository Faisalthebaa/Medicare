-- Step 2: Loading Staged Data into Production Schema
SET search_path TO production_medicare;

-- Load Patients
\copy patients FROM '/Users/danishraza/Documents/MediCare_Industry_Project/data/processed/clean_patients.csv' WITH (FORMAT csv, HEADER true);

-- Load Admissions
\copy admissions FROM '/Users/danishraza/Documents/MediCare_Industry_Project/data/processed/clean_admissions.csv' WITH (FORMAT csv, HEADER true);

-- Load Billing
\copy billing FROM '/Users/danishraza/Documents/MediCare_Industry_Project/data/processed/clean_billing.csv' WITH (FORMAT csv, HEADER true);

-- Load Lab Results
\copy lab_results FROM '/Users/danishraza/Documents/MediCare_Industry_Project/data/processed/clean_lab_results.csv' WITH (FORMAT csv, HEADER true);
