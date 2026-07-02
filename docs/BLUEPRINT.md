# 🏥 MediCare Advanced Analytics: Industry-Level Project Blueprint

## 1. Project Overview
This project simulates a real-world Healthcare Analytics environment. We move beyond simple data cleaning to build a full Data Warehouse, a Machine Learning pipeline, and a professional Business Intelligence (BI) suite.

**Goal:** Reduce 30-day hospital readmissions and optimize financial collection rates.
**Stakeholders:** Chief Medical Officer (CMO), Chief Financial Officer (CFO).

---

## 2. Technical Stack
- **Database:** PostgreSQL (The "Source of Truth" Data Warehouse).
- **Language:** Python (ETL, Data Validation, Machine Learning).
- **Libraries:** SQLAlchemy (DB connection), Pandas (Transformation), Scikit-Learn (Prediction).
- **BI Tool:** Tableau (Executive Dashboarding).

---

## 3. Data Architecture (The Pipeline)
1.  **Ingestion:** Python scripts load raw CSVs into a **Staging Schema** in PostgreSQL.
2.  **Cleaning & Transformation (ETL):** 
    - Handle NULL values in `days_to_readmit` and `outstanding_balance`.
    - Standardize date formats.
    - Create a **Production Schema** with normalized tables.
3.  **Analytical Layer:** Create SQL Views for:
    - `vw_revenue_summary`: Joins billing and admissions for financial analysis.
    - `vw_patient_risk_profile`: Combines clinical data with comorbidity scores.
4.  **Machine Learning:** Predict `readmitted_30d` based on patient metrics.
5.  **Visualization:** Tableau connects to PostgreSQL Views for real-time reporting.

---

## 4. Advanced "Senior-Level" Features
- **Data Validation:** Implement a script that flags "Bad Data" (e.g., discharge date before admission date).
- **Feature Engineering:** Calculate **Customer Lifetime Value (CLV)** and **Hospital Efficiency Score**.
- **Model Explainability:** Identify which factors (Age, Lab Flags, etc.) contribute most to readmission.

---

## 5. Delivery Phases (Our Checklist)

### Phase 1: Environment & Database Architecture
- [ ] Create Python Virtual Environment.
- [ ] Initialize PostgreSQL Database `medicare_db`.
- [ ] Design and create Schema (Patients, Admissions, Billing, Diagnoses, Labs).

### Phase 2: Professional ETL (Extract, Transform, Load)
- [ ] Build `database_manager.py` for DB connections.
- [ ] Build `etl_pipeline.py` to move CSV data into Postgres with error handling.
- [ ] Verify data integrity (Row counts, data types).

### Phase 3: Advanced Analytics & SQL Engineering
- [ ] Build complex SQL Views for Tableau.
- [ ] Perform Cohort Analysis (How do patients behave over time?).

### Phase 4: Machine Learning (Predictive Analytics)
- [ ] Train Readmission Risk Model.
- [ ] Save model and create a script to "Score" new patients.

### Phase 5: Tableau Dashboarding
- [ ] Connect Tableau to PostgreSQL.
- [ ] Build Executive Dashboard (Revenue, Growth, KPIs).
- [ ] Build Clinical Dashboard (Readmissions, Lab Abnormalities).

---

## 6. Success Metrics
- **Accuracy:** ML Model achieves >75% accuracy in predicting readmissions.
- **Automation:** The entire pipeline from CSV to DB is one-click.
- **Utility:** Tableau dashboards answer at least 10 critical business questions.
