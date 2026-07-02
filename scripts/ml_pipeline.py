"""
MediCare MAP 2026: Machine Learning Pipeline
--------------------------------------------
This script handles the 'AI-Ready' phase of the project. We pull refined data 
directly from our PostgreSQL Warehouse to train two key predictive models:
1. Patient Readmission Risk (Clinical focus)
2. Financial High-Risk Debt (CFO focus)

Author: MediCare Data Engineering Team
Date: June 2026
"""

import pandas as pd
import numpy as np
import joblib
import os
import sys
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder

# We need to reach back to the scripts/ folder to grab our Database Bridge
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
try:
    from scripts.database_manager import DatabaseManager
except ImportError:
    # Fallback for local execution
    from database_manager import DatabaseManager

def train_readmission_model(db):
    """
    Predicts the likelihood of a patient returning within 30 days.
    This helps the CMO (Chief Medical Officer) prioritize follow-ups.
    """
    print("\n" + "="*50)
    print("STEP 1: TRAINING THE CLINICAL READMISSION MODEL")
    print("="*50)
    
    # We join Clinical Performance with Patients to get that vital 'Comorbidity Score'
    # we identified as a top predictor during Phase 3 exploration.
    sql_query = """
    SELECT 
        v.age,
        v.gender,
        v.department,
        v.admission_type,
        v.length_of_stay,
        v.is_readmitted,
        p.comorbidity_score
    FROM production_medicare.v_clinical_performance v
    JOIN production_medicare.patients p ON v.patient_id = p.patient_id
    """
    
    print("-> Fetching live data from PostgreSQL Warehouse...")
    data = pd.read_sql(sql_query, db.get_engine())
    print(f"-> Success. Processing {len(data):,} records.")

    # --- Preprocessing & Feature Engineering ---
    # Computers don't like 'Cardiology' as a string, so we map them to numbers.
    gender_enc = LabelEncoder()
    dept_enc = LabelEncoder()
    type_enc = LabelEncoder()
    
    data['gender'] = gender_enc.fit_transform(data['gender'])
    data['department'] = dept_enc.fit_transform(data['department'])
    data['admission_type'] = type_enc.fit_transform(data['admission_type'])
    
    # We select features that are KNOWN at the time of discharge.
    # We intentionally exclude 'days_to_readmit' because that's 'future info' 
    # and would cause 'Data Leakage' (cheating).
    features = ['age', 'gender', 'department', 'admission_type', 'length_of_stay', 'comorbidity_score']
    X = data[features]
    y = data['is_readmitted']
    
    # 80/20 Split: Train on most, test on the rest to ensure we haven't just memorized the data.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # --- The Core Model ---
    # Using 'class_weight=balanced' is critical here. Since readmissions are the minority, 
    # we want the model to pay 10x more attention when it sees a returning patient.
    rf_model = RandomForestClassifier(
        n_estimators=150, 
        max_depth=10, 
        class_weight='balanced', 
        random_state=42
    )
    
    print("-> Training Random Forest Classifier (Optimized for Class Imbalance)...")
    rf_model.fit(X_train, y_train)
    
    # --- Performance Evaluation ---
    predictions = rf_model.predict(X_test)
    acc = accuracy_score(y_test, predictions)
    
    print(f"\n[MODEL PERFORMANCE] Overall Accuracy: {acc:.1%}")
    print("-" * 30)
    print(classification_report(y_test, predictions))
    
    # Feature Importance: Showing the 'Why' behind the 'What'
    imps = pd.Series(rf_model.feature_importances_, index=features).sort_values(ascending=False)
    print("\n[INSIGHT] Top Risk Factors Identified:")
    print(imps.head(5))
    
    # --- Save for Production ---
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_dir = os.path.join(base_dir, 'models')
    os.makedirs(model_dir, exist_ok=True)
    
    joblib.dump(rf_model, os.path.join(model_dir, 'readmission_model.pkl'))
    # We save the encoders too, otherwise we can't translate new incoming data!
    joblib.dump({
        'gender_enc': gender_enc,
        'dept_enc': dept_enc,
        'type_enc': type_enc,
        'feature_list': features
    }, os.path.join(model_dir, 'readmission_metadata.pkl'))
    print(f"\n-> Model & Metadata securely saved to '{model_dir}'")

def train_financial_risk_model(db):
    """
    Predicts if a patient will have 'High Risk Debt'. 
    Essential for the CFO to manage hospital cash flow.
    """
    print("\n" + "="*50)
    print("STEP 2: TRAINING THE FINANCIAL RISK MODEL")
    print("="*50)
    
    query = "SELECT total_amount, department, is_high_risk_debt FROM production_medicare.v_financial_integrity"
    
    print("-> Pulling billing data...")
    df = pd.read_sql(query, db.get_engine())
    
    # Encode 'Department'
    dept_enc = LabelEncoder()
    df['department'] = dept_enc.fit_transform(df['department'])
    df['is_high_risk_debt'] = df['is_high_risk_debt'].astype(int)
    
    X = df[['total_amount', 'department']]
    y = df['is_high_risk_debt']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Simple, fast model for financial screening
    fin_model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
    fin_model.fit(X_train, y_train)
    
    print(f"-> Financial Model Accuracy: {accuracy_score(y_test, fin_model.predict(X_test)):.1%}")
    
    # Save it
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_dir = os.path.join(base_dir, 'models')
    os.makedirs(model_dir, exist_ok=True)

    joblib.dump(fin_model, os.path.join(model_dir, 'financial_risk_model.pkl'))
    joblib.dump({'dept_enc': dept_enc}, os.path.join(model_dir, 'financial_risk_metadata.pkl'))
    print(f"-> Financial Risk model saved to '{model_dir}'")

if __name__ == "__main__":
    # Initialize our database bridge
    bridge = DatabaseManager()
    
    if bridge.test_connection():
        print("🚀 Starting MediCare ML Pipeline...")
        train_readmission_model(bridge)
        train_financial_risk_model(bridge)
        print("\n✨ Phase 4 Complete: Both models are trained and ready for Phase 5.")
    else:
        print("‼️ CRITICAL ERROR: Could not establish a secure connection to the database.")
        sys.exit(1)
