import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
import datetime

# Database Connection Setup
DB_USER = 'root'
DB_PASSWORD = 'password123'
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_NAME = 'healthcare_analytics'

engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
print("Connecting to MySQL Database...")

# Create Star Schema Tables & Views via SQL DDL
with engine.connect() as conn:
    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS Dim_Patient (
        Patient_ID INT PRIMARY KEY,
        Age_Group VARCHAR(20),
        Gender VARCHAR(10),
        Insurance_Type VARCHAR(50),
        Chronic_Condition_Flag INT
    );
    """))
    
    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS Dim_Doctor (
        Doctor_ID INT PRIMARY KEY,
        Doctor_Name VARCHAR(100),
        Specialty VARCHAR(50),
        Department VARCHAR(50)
    );
    """))
    
    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS Dim_Date (
        Date_Key DATE PRIMARY KEY,
        Full_Date DATE,
        Month INT,
        Month_Name VARCHAR(15),
        Quarter INT,
        Year INT,
        Day_Of_Week VARCHAR(15)
    );
    """))
    
    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS Fact_Admissions (
        Admission_ID INT PRIMARY KEY,
        Patient_ID INT,
        Doctor_ID INT,
        Admission_Date DATE,
        Discharge_Date DATE,
        Length_Of_Stay_Days INT,
        Readmitted_30Days_Flag INT,
        Total_Treatment_Cost DECIMAL(10,2),
        Admission_Type VARCHAR(30),
        FOREIGN KEY (Patient_ID) REFERENCES Dim_Patient(Patient_ID),
        FOREIGN KEY (Doctor_ID) REFERENCES Dim_Doctor(Doctor_ID),
        FOREIGN KEY (Admission_Date) REFERENCES Dim_Date(Date_Key)
    );
    """))
    conn.commit()

print("Star Schema tables created successfully.")

# Generate Synthetic Clinical Data
np.random.seed(42)
num_patients = 1000
patients_df = pd.DataFrame({
    'Patient_ID': range(1001, 1001 + num_patients),
    'Age_Group': np.random.choice(['18-35', '36-50', '51-65', '65+'], size=num_patients, p=[0.2, 0.25, 0.3, 0.25]),
    'Gender': np.random.choice(['Male', 'Female'], size=num_patients),
    'Insurance_Type': np.random.choice(['Medicare', 'Medicaid', 'Private', 'Uninsured'], size=num_patients, p=[0.35, 0.25, 0.3, 0.1]),
    'Chronic_Condition_Flag': np.random.choice([0, 1], size=num_patients, p=[0.4, 0.6])
})

doctors_df = pd.DataFrame({
    'Doctor_ID': range(501, 521),
    'Doctor_Name': [f"Dr. Provider_{i}" for i in range(1, 21)],
    'Specialty': np.random.choice(['Cardiology', 'Internal Medicine', 'Orthopedics', 'Neurology'], size=20),
    'Department': np.random.choice(['General Care', 'ICU', 'Emergency', 'Surgical'], size=20)
})

date_range = pd.date_range(start='2024-01-01', end='2025-12-31', freq='D')
date_df = pd.DataFrame({
    'Date_Key': date_range.date,
    'Full_Date': date_range.date,
    'Month': date_range.month,
    'Month_Name': date_range.strftime('%B'),
    'Quarter': date_range.quarter,
    'Year': date_range.year,
    'Day_Of_Week': date_range.strftime('%A')
})

num_admissions = 5000
adm_dates = np.random.choice(date_range.date, size=num_admissions)
length_of_stay = np.random.randint(1, 21, size=num_admissions)
discharge_dates = [adm + datetime.timedelta(days=int(los)) for adm, los in zip(adm_dates, length_of_stay)]
costs = np.round(length_of_stay * np.random.uniform(800, 1500, size=num_admissions), 2)
readmission_flags = np.random.choice([0, 1], size=num_admissions, p=[0.88, 0.12])

fact_admissions_df = pd.DataFrame({
    'Admission_ID': range(10001, 10001 + num_admissions),
    'Patient_ID': np.random.choice(patients_df['Patient_ID'], size=num_admissions),
    'Doctor_ID': np.random.choice(doctors_df['Doctor_ID'], size=num_admissions),
    'Admission_Date': adm_dates,
    'Discharge_Date': discharge_dates,
    'Length_Of_Stay_Days': length_of_stay,
    'Readmitted_30Days_Flag': readmission_flags,
    'Total_Treatment_Cost': costs,
    'Admission_Type': np.random.choice(['Emergency', 'Elective', 'Urgent'], size=num_admissions, p=[0.5, 0.3, 0.2])
})

# Load Data into MySQL
patients_df.to_sql('Dim_Patient', con=engine, if_exists='append', index=False)
doctors_df.to_sql('Dim_Doctor', con=engine, if_exists='append', index=False)
date_df.to_sql('Dim_Date', con=engine, if_exists='append', index=False)
fact_admissions_df.to_sql('Fact_Admissions', con=engine, if_exists='append', index=False)

print("ETL Success: Data loaded into MySQL!")
