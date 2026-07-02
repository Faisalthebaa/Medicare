CREATE SCHEMA IF NOT EXISTS production_medicare;
SET search_path TO production_medicare;

CREATE TABLE IF NOT EXISTS patients (
    patient_id VARCHAR(10) PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    date_of_birth DATE,
    age INT,
    gender VARCHAR(5),
    blood_group VARCHAR(5),
    insurance_type VARCHAR(20),
    comorbidity_score INT,
    city VARCHAR(50),
    source_file VARCHAR(50),
    load_timestamp TIMESTAMP
);

CREATE TABLE IF NOT EXISTS admissions (
    admission_id VARCHAR(10) PRIMARY KEY,
    patient_id VARCHAR(10),
    department VARCHAR(50),
    admission_date DATE NOT NULL,
    discharge_date DATE,
    length_of_stay INT,
    wait_time_hours DECIMAL(5,2),
    admission_type VARCHAR(20),
    outcome VARCHAR(20),
    readmitted_30d INT,
    days_to_readmit DECIMAL(5,1),
    attending_doctor VARCHAR(10),
    source_file VARCHAR(50),
    load_timestamp TIMESTAMP,
    etl_integrity_status VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS billing (
    bill_id VARCHAR(10) PRIMARY KEY,
    admission_id VARCHAR(10),
    patient_id VARCHAR(10),
    total_amount DECIMAL(12,2),
    amount_paid DECIMAL(12,2),
    outstanding_balance DECIMAL(12,2),
    payment_status VARCHAR(20),
    insurance_type VARCHAR(20),
    source_file VARCHAR(50),
    load_timestamp TIMESTAMP,
    is_high_risk_debt BOOLEAN
);

CREATE TABLE IF NOT EXISTS lab_results (
    lab_id VARCHAR(15) PRIMARY KEY,
    admission_id VARCHAR(10),
    patient_id VARCHAR(10),
    test_name VARCHAR(50),
    result_value DECIMAL(10,2),
    flag VARCHAR(100),
    test_date DATE,
    source_file VARCHAR(50),
    load_timestamp TIMESTAMP
);
