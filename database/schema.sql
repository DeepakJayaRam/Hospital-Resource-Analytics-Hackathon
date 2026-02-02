-- ------------------------------------------------------------------
-- OpsPulse Hospital Intelligence - Database Schema
-- Run this script in PostgreSQL to initialize the database structure.
-- ------------------------------------------------------------------

-- 1. CLEANUP
-- Drop tables in reverse order of dependencies to avoid Foreign Key errors
DROP TABLE IF EXISTS admissions;
DROP TABLE IF EXISTS doctors;
DROP TABLE IF EXISTS patients;
DROP TABLE IF EXISTS departments;

-- 2. CREATE TABLES

-- Table: Departments
-- Stores hospital capacity and structural info
CREATE TABLE departments (
    dept_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,       -- e.g., 'Cardiology', 'Neurology'
    branch VARCHAR(50) NOT NULL,     -- e.g., 'Main Block', 'East Wing'
    total_beds INT NOT NULL          -- Max capacity for occupancy calc
);

-- Table: Doctors
-- Links staff to specific departments
CREATE TABLE doctors (
    doc_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    dept_id INT REFERENCES departments(dept_id),
    specialty VARCHAR(50)            -- e.g., 'Surgeon', 'Consultant'
);

-- Table: Patients
-- Static patient demographics
CREATE TABLE patients (
    patient_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT,
    gender VARCHAR(10),              -- 'M', 'F', 'Other'
    city VARCHAR(50)                 -- Useful for heatmaps
);

-- Table: Admissions (The Transactional Core)
-- Tracks every visit, stay duration, and outcome
CREATE TABLE admissions (
    admission_id SERIAL PRIMARY KEY,
    patient_id INT REFERENCES patients(patient_id),
    doc_id INT REFERENCES doctors(doc_id),
    dept_id INT REFERENCES departments(dept_id),
    
    admission_date TIMESTAMP NOT NULL,
    discharge_date TIMESTAMP,        -- NULL indicates the patient is CURRENTLY admitted
    
    admission_type VARCHAR(20),      -- 'Emergency' or 'Elective'
    outcome VARCHAR(50),             -- 'Recovered', 'Transferred', 'Deceased', or NULL (if active)
    billing_amount DECIMAL(10, 2)    -- For Revenue KPIs
);

-- 3. INDEXING (Optional but Good for Performance)
-- Speed up queries on frequently filtered columns
CREATE INDEX idx_admissions_dept ON admissions(dept_id);
CREATE INDEX idx_admissions_status ON admissions(discharge_date); -- Speeds up "Active Patients" queries