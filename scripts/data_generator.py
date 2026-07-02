"""
MediCare MAP 2026: Big Data Generator (V5.Cultural Consistency)
Chief Data Strategist: Danish Raza
Goal: 30k+ rows, 15-16% readmit, and Culturally Consistent Personas.
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# ── CONFIGURATION ─────────────────────────────────────────────────────────────
NP_SEED = 42
RANDOM_SEED = 42
np.random.seed(NP_SEED)
random.seed(RANDOM_SEED)

TARGET_PATH = "/Users/danishraza/Documents/MediCare_Industry_Project/data/raw/"
os.makedirs(TARGET_PATH, exist_ok=True)

# ── CULTURAL NAME POOLS ───────────────────────────────────────────────────────
NAME_POOLS = {
    "Hindu": {
        "first": ["Aarav", "Priya", "Rohan", "Anjali", "Vikram", "Meera", "Arjun", "Sunita", "Ravi", "Kavya", "Sanjay", "Deepa"],
        "last": ["Sharma", "Patel", "Kumar", "Singh", "Verma", "Nair", "Reddy", "Iyer", "Das", "Bose"]
    },
    "Muslim": {
        "first": ["Fatima", "Omar", "Zaid", "Sana", "Ahmed", "Aisha", "Kabir", "Zara", "Hamza", "Mariam", "Mustafa", "Leyla"],
        "last": ["Khan", "Ali", "Ahmed", "Sheikh", "Sayed", "Qureshi", "Malik", "Hussain", "Farooqui", "Siddiqui"]
    },
    "Foreign": {
        "first": ["James", "Sarah", "Michael", "Emily", "David", "Sophia", "John", "Olivia", "Robert", "Emma", "William", "Mia"],
        "last": ["Smith", "Johnson", "Williams", "Brown", "Jones", "Davis", "Wilson", "Anderson", "Taylor", "Thomas"]
    }
}

DEPARTMENTS = ["Emergency", "Cardiology", "Oncology", "Orthopedics", "Neurology", "Pediatrics", "General Medicine", "ICU"]
INSURANCE = ["Medicare", "Medicaid", "Private", "Self-pay", "Government"]
CITIES = ["Bengaluru", "Mumbai", "Delhi", "Chennai", "Hyderabad", "Pune", "Kolkata", "Ahmedabad"]

DIAGNOSES = {
    "I21": "Acute myocardial infarction", "J18": "Pneumonia", "N39": "Urinary tract infection",
    "E11": "Type 2 diabetes mellitus", "I50": "Heart failure", "J44": "COPD",
    "S72": "Fracture of femur", "C34": "Malignant neoplasm of bronchus/lung",
    "G35": "Multiple sclerosis", "K92": "GI haemorrhage", "I63": "Cerebral infarction",
    "F32": "Depressive episode", "A41": "Sepsis", "N17": "Acute kidney failure",
    "J96": "Respiratory failure"
}

# ── 1. PATIENTS (1,200 Rows) ──────────────────────────────────────────────────
def generate_patients(n=1200):
    records = []
    for i in range(1, n + 1):
        dob = datetime(1940, 1, 1) + timedelta(days=random.randint(0, 365 * 75))
        age = (datetime(2024, 1, 1) - dob).days // 365
        gender = random.choice(["M", "F"])
        insurance = np.random.choice(INSURANCE, p=[0.30, 0.20, 0.35, 0.10, 0.05])
        blood_group = random.choice(["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        
        # Consistent Name Selection
        category = random.choice(list(NAME_POOLS.keys()))
        first_name = random.choice(NAME_POOLS[category]["first"])
        last_name = random.choice(NAME_POOLS[category]["last"])

        base_comorb = 1.0 if age < 40 else (1.5 if age < 65 else 2.5)
        comorbidity_score = int(np.clip(np.random.poisson(base_comorb), 0, 6))

        records.append({
            "patient_id": f"P{i:05d}",
            "first_name": first_name,
            "last_name": last_name,
            "date_of_birth": dob.strftime("%Y-%m-%d"),
            "age": age,
            "gender": gender,
            "blood_group": blood_group,
            "insurance_type": insurance,
            "comorbidity_score": comorbidity_score,
            "city": random.choice(CITIES),
        })
    return pd.DataFrame(records)

# ── 2. ADMISSIONS (4,000 Rows) ────────────────────────────────────────────────
def generate_admissions(patients_df, n=4000):
    records = []
    for i in range(1, n + 1):
        patient = patients_df.sample(1).iloc[0]
        age, comorb = patient["age"], patient["comorbidity_score"]
        dept = np.random.choice(DEPARTMENTS, p=[0.20, 0.15, 0.10, 0.10, 0.10, 0.08, 0.17, 0.10])
        admit_date = datetime(2022, 1, 1) + timedelta(days=random.randint(0, 730))
        base_los = max(1, int(np.random.exponential(3)))
        mult = 1.0 + (0.5 if dept in ["ICU", "Oncology"] else 0) + (0.3 if age > 70 else 0) + (0.4 if comorb > 3 else 0)
        los = int(np.clip(base_los * mult, 1, 45))
        risk_score = (age / 100) * 0.4 + (comorb / 6) * 0.5 + (0.1 if dept == "Emergency" else 0)
        readmitted = 1 if random.random() < (risk_score * 0.49) else 0
        
        records.append({
            "admission_id": f"A{i:06d}",
            "patient_id": patient["patient_id"],
            "department": dept,
            "admission_date": admit_date.strftime("%Y-%m-%d"),
            "discharge_date": (admit_date + timedelta(days=los)).strftime("%Y-%m-%d"),
            "length_of_stay": los,
            "wait_time_hours": round(np.clip(np.random.exponential(2.5), 0.5, 18), 1),
            "admission_type": np.random.choice(["Emergency", "Elective", "Urgent"], p=[0.40, 0.45, 0.15]),
            "outcome": "Discharged",
            "readmitted_30d": readmitted,
            "days_to_readmit": random.randint(3, 30) if readmitted else None,
            "attending_doctor": f"DR{random.randint(1, 80):03d}"
        })
    return pd.DataFrame(records)

# ── 3. DIAGNOSES (~11,500 Rows) ───────────────────────────────────────────────
def generate_diagnoses(admissions_df):
    records = []
    for _, adm in admissions_df.iterrows():
        n_diag = random.randint(2, 4)
        selected_codes = random.sample(list(DIAGNOSES.keys()), n_diag)
        for rank, code in enumerate(selected_codes, 1):
            records.append({
                "diagnosis_id": f"D{len(records)+1:07d}",
                "admission_id": adm["admission_id"],
                "patient_id": adm["patient_id"],
                "icd10_code": code,
                "diagnosis_name": DIAGNOSES[code],
                "diagnosis_rank": rank,
                "severity": random.choice(["Mild", "Moderate", "Severe"]) if rank > 1 else "Severe"
            })
    return pd.DataFrame(records)

# ── 4. LAB RESULTS (~24,000 Rows) ─────────────────────────────────────────────
def generate_lab_results(admissions_df):
    records = []
    tests = {"Hemoglobin":(13.5,17.5),"WBC":(4.5,11.0),"Platelets":(150,400),"Creatinine":(0.6,1.2),"Glucose":(70,100), "Sodium":(136,145), "Potassium":(3.5,5.0)}
    for _, adm in admissions_df.iterrows():
        abnormal_chance = 0.4 if adm["readmitted_30d"] == 1 else 0.15
        selected_tests = random.sample(list(tests.items()), random.randint(5, 7))
        for name, (low, high) in selected_tests:
            is_abnormal = random.random() < abnormal_chance
            val = random.uniform(high+1, high+20) if is_abnormal else random.uniform(low, high)
            records.append({
                "lab_id": f"L{len(records)+1:08d}",
                "admission_id": adm["admission_id"],
                "patient_id": adm["patient_id"],
                "test_name": name,
                "result_value": round(val, 2),
                "flag": "High" if is_abnormal else "Normal",
                "test_date": adm["admission_date"]
            })
    return pd.DataFrame(records)

# ── 5. BILLING (4,000 Rows) ───────────────────────────────────────────────────
def generate_billing(admissions_df, patients_df):
    df = admissions_df.merge(patients_df[['patient_id', 'insurance_type']], on='patient_id')
    records = []
    for _, row in df.iterrows():
        base = row["length_of_stay"] * 1200 + random.uniform(500, 5000)
        ratio = random.uniform(0.1, 0.5) if row["insurance_type"] == "Self-pay" else random.uniform(0.8, 1.0)
        paid = round(base * ratio, 2)
        records.append({
            "bill_id": f"B{len(records)+1:06d}",
            "admission_id": row["admission_id"],
            "patient_id": row["patient_id"],
            "total_amount": round(base, 2),
            "amount_paid": paid,
            "outstanding_balance": round(base - paid, 2),
            "payment_status": "Paid" if (base-paid) < 10 else "Partial",
            "insurance_type": row["insurance_type"]
        })
    return pd.DataFrame(records)

# ── EXECUTION ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("🚀 Fixing Cultural Consistency & Refreshing 45k rows...")
    p = generate_patients(1200)
    a = generate_admissions(p, 4000)
    d = generate_diagnoses(a)
    l = generate_lab_results(a)
    b = generate_billing(a, p)

    p.to_csv(TARGET_PATH + "patients.csv", index=False)
    a.to_csv(TARGET_PATH + "admissions.csv", index=False)
    d.to_csv(TARGET_PATH + "diagnoses.csv", index=False)
    l.to_csv(TARGET_PATH + "lab_results.csv", index=False)
    b.to_csv(TARGET_PATH + "billing.csv", index=False)

    total_rows = len(p) + len(a) + len(d) + len(l) + len(b)
    print(f"✅ Refresh Complete!")
    print(f"📈 Total Rows: {total_rows:,} | Readmit Rate: {a['readmitted_30d'].mean()*100:.2f}%")
    print(f"👤 Sample (Hindu):   {p[p['last_name'].isin(NAME_POOLS['Hindu']['last'])].iloc[0][['first_name','last_name']].values}")
    print(f"👤 Sample (Muslim):  {p[p['last_name'].isin(NAME_POOLS['Muslim']['last'])].iloc[0][['first_name','last_name']].values}")
    print(f"👤 Sample (Foreign): {p[p['last_name'].isin(NAME_POOLS['Foreign']['last'])].iloc[0][['first_name','last_name']].values}")
