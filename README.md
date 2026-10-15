# Enterprise Healthcare Readmission & Clinical Resource Analytics System

## 🚀 Project Overview
An end-to-end healthcare data analytics solution designed to track, monitor, and mitigate unplanned 30-day patient readmissions under CMS HRRP standards. This project transitions raw operational data into high-impact executive insights to reduce financial penalty exposure.

## 🛠️ Tech Stack
* **Database & Modeling:** MySQL (Star Schema, Primary/Foreign Keys, Performance Views)
* **Data Engineering:** Python (`pandas`, `sqlalchemy`, `pymysql`) for automated ETL pipelines and data validation
* **Business Intelligence:** Power BI Desktop (Power Query, DAX Engine, Executive Dashboarding)
* **Version Control:** Git & GitHub

## 📊 Architecture & Schema Design
The data model uses a 1-to-Many Star Schema comprising:
* **Fact Table:** `Fact_Admissions` (Transactional records, stay durations, costs, readmission flags)
* **Dimension Tables:** `Dim_Patient`, `Dim_Doctor`, `Dim_Date`

## 📐 Key DAX Measures
* **30-Day Readmission Rate %:** Tracks performance against target benchmarks.
* **Average Length of Stay (ALOS):** Evaluates resource efficiency across hospital departments.
* **Readmission Financial Penalty:** Isolates treatment costs tied directly to 30-day readmissions.

## 📈 Executive Dashboard Highlights
* **Page 1 (Clinical Operations):** Real-time KPI tracking, monthly trend analysis against target benchmarks, and doctor/specialty bottleneck matrix.
* **Page 2 (Demographics & Financial Risk):** Patient age-group analysis, chronic condition status breakdowns, and cost vs. length of stay correlations.
