MediCare MAP – Healthcare Data Analytics Platform

Overview

MediCare MAP is an end-to-end healthcare data engineering and analytics project built to demonstrate how raw hospital data can be transformed into meaningful business insights.

The project integrates patient admissions, billing information, laboratory results, diagnoses, and doctor details into a centralized PostgreSQL database. A complete ETL pipeline was developed to clean and validate the data before storing it in an analytical warehouse, where SQL views and machine learning models generate actionable insights for healthcare management.

The objective of this project is to showcase practical data engineering, SQL, analytics, and machine learning skills using a real-world healthcare use case.

⸻

Problem Statement

Hospitals often maintain patient records across multiple independent systems. This makes it difficult to perform comprehensive analysis, identify patient trends, and make informed operational decisions.

This project addresses those challenges by:

* Integrating data from multiple hospital sources
* Building a centralized analytical database
* Automating data validation and cleaning
* Generating business insights using SQL
* Predicting clinical and financial risks using machine learning

⸻

Project Objectives

* Design a scalable healthcare database
* Build a reliable ETL pipeline
* Perform analytical SQL queries
* Create reusable reporting views
* Predict patient readmission risk
* Predict high-risk billing accounts
* Prepare clean data for dashboard development

⸻

Tech Stack

Programming Language

* Python

Database

* PostgreSQL

Libraries

* Pandas
* NumPy
* Scikit-learn

Machine Learning

* Random Forest Classifier

Tools

* PostgreSQL
* pgAdmin
* Jupyter Notebook
* Git
* GitHub

⸻

Database Design

The project uses a normalized relational database consisting of seven core tables.

* Patients
* Admissions
* Doctors
* Billing
* Lab Results
* Diagnoses
* Departments

Relationships are created using primary and foreign keys to maintain data integrity and eliminate redundancy.

⸻

ETL Pipeline

The ETL process performs several preprocessing tasks before loading the data into PostgreSQL.

Some of the key transformations include:

* Removing duplicate records
* Handling missing values
* Standardizing date formats
* Validating admission and discharge dates
* Data quality checks
* Logging invalid records separately for review

This ensures that only clean and validated data is stored in the production database.

⸻

SQL Analytics

Several SQL views were created to simplify reporting and analysis.

The project includes analysis such as:

* Patient readmission trends
* Department-wise performance
* Billing analysis
* Insurance-wise payment statistics
* Hospital revenue insights
* Patient demographics
* Clinical performance metrics

⸻

Machine Learning

A Random Forest classification model was trained to identify patients with a higher probability of readmission.

The project also predicts financially high-risk accounts using hospital billing information.

The trained models help demonstrate how predictive analytics can support both healthcare providers and hospital administration.

⸻

Key Features

* End-to-end healthcare analytics project
* Relational database design
* Automated ETL pipeline
* Data validation framework
* Analytical SQL reporting
* Machine learning integration
* Production-ready database structure
* Dashboard-ready dataset

Project Structure
MediCare-MAP/
│
├── data/
│   ├── raw_data
│   ├── processed_data
│
├── database/
│   ├── schema.sql
│   ├── tables.sql
│   ├── views.sql
│
├── etl/
│   ├── etl_pipeline.py
│
├── notebooks/
│
├── machine_learning/
│   ├── model_training.py
│   ├── saved_models
│
├── reports/
│
├── screenshots/
│
└── README.md

Future Improvements

Some planned enhancements include:

* Interactive Tableau dashboard
* Power BI dashboard
* Real-time data ingestion
* REST API integration
* Automated scheduling using Apache Airflow
* Cloud deployment using AWS or Azure

⸻

Learning Outcomes

This project strengthened my understanding of:

* Database design
* SQL optimization
* Data cleaning
* ETL development
* Data warehousing
* Machine learning workflows
* Healthcare analytics
* Version control using Git

⸻

About the Project

This project was developed as part of my learning journey to gain practical experience in Data Engineering, SQL, Analytics, and Machine Learning. It demonstrates the complete workflow from raw healthcare data to predictive analytics and business-ready datasets.
