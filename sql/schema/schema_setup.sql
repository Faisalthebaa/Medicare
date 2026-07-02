-- MediCare MAP 2026: Master Schema Setup
-- Author: Danish Raza, Chief Data Strategist
-- Goal: Establish a high-performance relational warehouse for clinical & financial data.

-- 1. Create Schema for organization
CREATE SCHEMA IF NOT EXISTS production_medicare;
SET search_path TO production_medicare;

-- 2. Patients Table (Dimension)
-- Stores demographic data for risk stratification.
CREATE TABLE IF NOT EXISTS patients (
    patient_id VARCHAR(10) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE,
    age INT,
    gender VARCHAR(1),
    blood_group VARCHAR(5),
    insurance_type VARCHAR(20),
    comorbidity_score INT,
    city VARCHAR(50),
    -- ETL Metadata
    source_file VARCHAR(50),
    load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Admissions Table (Fact)
-- The central hub of hospital activity.
CREATE TABLE IF NOT EXISTS admissions (
    admission_id VARCHAR(10) PRIMARY KEY,
    patient_id VARCHAR(10) REFERENCES patients(patient_id),
    department VARCHAR(50),
    admission_date DATE NOT NULL,
    discharge_date DATE,
    length_of_stay INT,
    wait_time_hours DECIMAL(5,2),
    admission_type VARCHAR(20),
    outcome VARCHAR(20),
    readmitted_30d INT DEFAULT 0,
    days_to_readmit DECIMAL(5,1),
    attending_doctor VARCHAR(10),
    -- ETL Metadata & Integrity Flags
    etl_integrity_status VARCHAR(100) DEFAULT 'Verified',
    source_file VARCHAR(50),
    load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Billing Table (Fact)
-- Tracks the $1.2M revenue potential.
CREATE TABLE IF NOT EXISTS billing (
    bill_id VARCHAR(10) PRIMARY KEY,
    admission_id VARCHAR(10) REFERENCES admissions(admission_id),
    patient_id VARCHAR(10) REFERENCES patients(patient_id),
    room_charges DECIMAL(12,2),
    medication_charges DECIMAL(12,2),
    procedure_charges DECIMAL(12,2),
    lab_charges DECIMAL(12,2),
    total_amount DECIMAL(12,2),
    amount_paid DECIMAL(12,2),
    outstanding_balance DECIMAL(12,2),
    payment_status VARCHAR(20),
    insurance_type VARCHAR(20),
    -- ETL Metadata
    is_high_risk_debt BOOLEAN DEFAULT FALSE,
    source_file VARCHAR(50),
    load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Diagnoses Table (Dimension)
-- Stores medical codes (ICD-10) for AI feature importance.
CREATE TABLE IF NOT EXISTS diagnoses (
    diagnosis_id VARCHAR(10) PRIMARY KEY,
    admission_id VARCHAR(10) REFERENCES admissions(admission_id),
    patient_id VARCHAR(10) REFERENCES patients(patient_id),
    icd10_code VARCHAR(10),
    diagnosis_name VARCHAR(100),
    diagnosis_rank INT,
    severity VARCHAR(20),
    -- ETL Metadata
    source_file VARCHAR(50),
    load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Lab Results Table (Fact)
-- Critical clinical markers for Phase 3 AI predictions.
CREATE TABLE IF NOT EXISTS lab_results (
    lab_id VARCHAR(15) PRIMARY KEY,
    admission_id VARCHAR(10) REFERENCES admissions(admission_id),
    patient_id VARCHAR(10) REFERENCES patients(patient_id),
    test_name VARCHAR(50),
    result_value DECIMAL(10,2),
    reference_low DECIMAL(10,2),
    reference_high DECIMAL(10,2),
    flag VARCHAR(100), -- Increased for Clinical Sanity warnings
    test_date DATE,
    -- ETL Metadata
    source_file VARCHAR(50),
    load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. Indexes for Tableau Performance
CREATE INDEX IF NOT EXISTS idx_admission_date ON admissions(admission_date);
CREATE INDEX IF NOT EXISTS idx_patient_readmit ON admissions(readmitted_30d);
CREATE INDEX IF NOT EXISTS idx_billing_status ON billing(payment_status);
