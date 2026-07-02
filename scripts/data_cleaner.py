import pandas as pd
import numpy as np

class DataCleaner:
    """
    The Intelligence Layer for MediCare 2026.
    Implements Clinical Sanity, Date Integrity, and Flagging.
    """
    
    @staticmethod
    def parse_date(date_str):
        """Attempts to standardize dates into YYYY-MM-DD."""
        if pd.isna(date_str) or str(date_str).strip() == "":
            return pd.NaT
        
        # Trial and Error parsing for robustness
        formats = ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d', '%Y-%m-%dT%H:%M:%S']
        for fmt in formats:
            try:
                return pd.to_datetime(date_str, format=fmt)
            except:
                continue
        # Fallback to pandas generic parser
        try:
            return pd.to_datetime(date_str)
        except:
            return pd.NaT

    def clean_patients(self, df):
        """Standardizes Patient demographic data."""
        df = df.copy()
        # Ensure consistent ID format
        df['patient_id'] = df['patient_id'].astype(str).str.strip().str.upper()
        # Parse DOB
        if 'date_of_birth' in df.columns:
            df['date_of_birth'] = df['date_of_birth'].apply(self.parse_date)
        # Standardize Gender
        if 'gender' in df.columns:
            df['gender'] = df['gender'].str.strip().str.upper().str[0]
        return df

    def clean_admissions(self, df):
        """Processes Admission and Discharge logic with Hierarchy Rules."""
        df = df.copy()
        
        # 1. Standardize Dates
        df['admission_date'] = df['admission_date'].apply(self.parse_date)
        df['discharge_date'] = df['discharge_date'].apply(self.parse_date)
        
        # 2. Mandatory Check: Track rows without Admission Date for Quarantine
        # We don't drop here, we flag, so the pipeline can decide.
        df['etl_integrity_status'] = 'Verified'
        df.loc[df['admission_date'].isna(), 'etl_integrity_status'] = 'Quarantine: Missing Admission Date'
        
        # 3. Integrity Flagging (Approach 2)
        # Rule: Discharge before Admission
        mask_chrono = (df['discharge_date'] < df['admission_date'])
        df.loc[mask_chrono, 'etl_integrity_status'] = 'Review Required: Chronology Error'
        
        # Rule: Discharged status but no date (Logic Error)
        if 'outcome' in df.columns:
            mask_logic = (df['outcome'].str.lower() == 'discharged') & (df['discharge_date'].isna())
            df.loc[mask_logic, 'etl_integrity_status'] = 'Review Required: Missing Discharge Date'
        
        # 4. Calculate Derived Metrics (Value Add)
        mask_valid_dates = df['admission_date'].notna() & df['discharge_date'].notna() & (~mask_chrono)
        df.loc[mask_valid_dates, 'length_of_stay'] = (df['discharge_date'] - df['admission_date']).dt.days
            
        return df

    def clinical_sanity_check(self, df):
        """
        Flags impossible clinical values (Clinical Sanity Pillar).
        """
        df = df.copy()
        if 'test_name' in df.columns and 'result_value' in df.columns:
            # Initialize flag column if it doesn't exist
            if 'flag' not in df.columns:
                df['flag'] = 'Normal'
            
            # Hard Bound: SpO2 cannot exceed 100
            mask_spo2 = (df['test_name'].str.contains('Oxygen|SpO2', case=False)) & (df['result_value'] > 100)
            df.loc[mask_spo2, 'flag'] = 'Critical: Sensor Error (Value > 100)'
            
            # Soft Bound: Fever Alert (> 105F)
            mask_fever = (df['test_name'].str.contains('Temp', case=False)) & (df['result_value'] > 105)
            df.loc[mask_fever, 'flag'] = 'High Severity: Clinical Review Needed'
            
        return df

    def apply_financial_stratification(self, df):
        """
        Implements the 0-90 / 90+ Day Buckets logic.
        """
        df = df.copy()
        if 'outstanding_balance' in df.columns:
            df['is_high_risk_debt'] = False
            # Logic: If balance > 5000 and status is Overdue, flag as high risk
            mask_risk = (df['outstanding_balance'] > 5000) & (df['payment_status'] == 'Overdue')
            df.loc[mask_risk, 'is_high_risk_debt'] = True
            
        return df

    def clean_diagnoses(self, df):
        """Standardizes Diagnosis and ICD-10 data."""
        df = df.copy()
        if 'icd10_code' in df.columns:
            df['icd10_code'] = df['icd10_code'].str.strip().str.upper()
        return df
