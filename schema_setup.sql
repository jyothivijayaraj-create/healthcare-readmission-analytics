-- Create Database
CREATE DATABASE IF NOT EXISTS healthcare_analytics;
USE healthcare_analytics;

-- 1. Patient Dimension Table
CREATE TABLE IF NOT EXISTS Dim_Patient (
    Patient_ID INT PRIMARY KEY,
    Age_Group VARCHAR(20),
    Gender VARCHAR(10),
    Insurance_Type VARCHAR(50),
    Chronic_Condition_Flag INT
);

-- 2. Doctor Dimension Table
CREATE TABLE IF NOT EXISTS Dim_Doctor (
    Doctor_ID INT PRIMARY KEY,
    Doctor_Name VARCHAR(100),
    Specialty VARCHAR(50),
    Department VARCHAR(50)
);

-- 3. Date Dimension Table
CREATE TABLE IF NOT EXISTS Dim_Date (
    Date_Key DATE PRIMARY KEY,
    Full_Date DATE,
    Month INT,
    Month_Name VARCHAR(15),
    Quarter INT,
    Year INT,
    Day_Of_Week VARCHAR(15)
);

-- 4. Admissions Fact Table
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

-- 5. Executive Readmission Summary View
CREATE OR REPLACE VIEW vw_ReadmissionSummary AS
SELECT 
    p.Insurance_Type,
    COUNT(f.Admission_ID) AS Total_Admissions,
    SUM(f.Readmitted_30Days_Flag) AS Total_Readmissions,
    AVG(f.Length_Of_Stay_Days) AS Avg_Length_Of_Stay,
    SUM(f.Total_Treatment_Cost) AS Total_Financial_Impact
FROM Fact_Admissions f
JOIN Dim_Patient p ON f.Patient_ID = p.Patient_ID
GROUP BY p.Insurance_Type;
