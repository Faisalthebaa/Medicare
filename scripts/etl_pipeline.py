import pandas as pd
import os
from datetime import datetime
import sys

# Import our custom modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Note: We still import DatabaseManager for path consistency, but won't use it for loading.
from data_cleaner import DataCleaner

class ETLPipeline:
    """
    The Main Conductor for the MediCare 2026 Project.
    Orchestrates the flow from Raw CSV -> Clean Python -> Staged Processed Files.
    """
    
    def __init__(self):
        self.cleaner = DataCleaner()
        self.raw_data_path = "../../data/raw/"
        self.processed_path = "../../data/processed/"
        self.quarantine_path = "../../data/quarantine/"
        
        # Ensure directories exist
        for path in [self.processed_path, self.quarantine_path]:
            os.makedirs(os.path.abspath(os.path.join(os.path.dirname(__file__), path)), exist_ok=True)

    def process_file(self, file_name, table_name, cleaning_func=None):
        """Standard process for each file: Load, Clean, Stage."""
        print(f"\n📂 Processing {file_name}...")
        
        # 1. Load Raw Data
        full_path = os.path.abspath(os.path.join(os.path.dirname(__file__), self.raw_data_path, file_name))
        try:
            df = pd.read_csv(full_path)
        except Exception as e:
            print(f"❌ Error reading {file_name}: {e}")
            return

        # 2. Add Metadata (Lineage Pillar)
        df['source_file'] = file_name
        df['load_timestamp'] = datetime.now()
        
        # 3. Apply Custom Cleaning Logic (The Brain)
        if cleaning_func:
            df = cleaning_func(df)
            
        # 4. Quarantine Logic (Integrity Pillar)
        # If the cleaner flagged anything as 'Quarantine', move it to a separate file
        if 'etl_integrity_status' in df.columns:
            quarantine_mask = df['etl_integrity_status'].str.startswith('Quarantine', na=False)
            if quarantine_mask.any():
                quarantine_df = df[quarantine_mask]
                df = df[~quarantine_mask]
                
                q_path = os.path.abspath(os.path.join(os.path.dirname(__file__), self.quarantine_path, f"quarantine_{file_name}"))
                quarantine_df.to_csv(q_path, index=False)
                print(f"⚠️  Quarantined: {len(quarantine_df)} rows moved to '{q_path}'.")

        # 5. Stage to Processed Folder (The Handover)
        # We save as CSV for easy inspection and SQL loading by the user
        processed_file = os.path.abspath(os.path.join(os.path.dirname(__file__), self.processed_path, f"clean_{file_name}"))
        df.to_csv(processed_file, index=False)
        print(f"✅ Success: {len(df)} clean rows staged at '{processed_file}'.")

    def run_full_pipeline(self):
        """The Hierarchical Load Sequence."""
        print("🚀 Starting MediCare 2026 Industry-Level ETL Pipeline (Transformation Phase)...")
        
        # 1. Patients (The Foundation)
        self.process_file('patients.csv', 'patients', cleaning_func=self.cleaner.clean_patients)
        
        # 2. Admissions (The Activity - with special Date Logic)
        self.process_file('admissions.csv', 'admissions', cleaning_func=self.cleaner.clean_admissions)
        
        # 3. Details (Depends on Patients and Admissions)
        self.process_file('billing.csv', 'billing', cleaning_func=self.cleaner.apply_financial_stratification)
        self.process_file('diagnoses.csv', 'diagnoses', cleaning_func=self.cleaner.clean_diagnoses)
        self.process_file('lab_results.csv', 'lab_results', cleaning_func=self.cleaner.clinical_sanity_check)
        
        print("\n🏆 ETL Transformation Complete. Clean datasets are ready for SQL analysis.")

if __name__ == "__main__":
    pipeline = ETLPipeline()
    pipeline.run_full_pipeline()
