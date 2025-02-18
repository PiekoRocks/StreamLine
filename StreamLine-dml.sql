-- DML.sql - Data Manipulation Queries for StreamLine Web Application

-- ================================
-- NOTE: The colon (:) character is used to denote variables
-- that will receive values from the backend programming language.
-- ================================

-- ================================
-- DELETE Queries - Ensure Proper Cascade Deletion for Many-to-Many Relationships
-- ================================
DELETE FROM Workers_Inspections WHERE worker_id = 201;
DELETE FROM Workers_Inspections WHERE inspection_id = 5;
DELETE FROM Hydrants_Inspections WHERE hydrant_id = 101;
DELETE FROM Hydrants_Inspections WHERE inspection_id = 3;

-- ================================
-- INSERT Queries - Adding Records to Tables
-- ================================

-- Regions Table
INSERT INTO Regions (county_name, region_name) 
VALUES ('Benton', 'Downtown');

-- Workers Table
INSERT INTO Workers (region_id, name, salary, assigned_date) 
VALUES (101, 'John Smith', 50000, '2024-12-01');

-- Hydrants Table
INSERT INTO Hydrants (region_id, flow_rate, is_operational, gps_long, gps_lat) 
VALUES (101, 1500, TRUE, -23.0455, 50.2865);

-- Inspections Table
INSERT INTO Inspections (inspection_date, inspection_completed, note) 
VALUES ('2025-02-01', TRUE, 'Minor damage');

-- Maintenance Logs Table
INSERT INTO Maintenance_Logs (maint_hydrant_id, maint_cost, maint_needed) 
VALUES (1, 150, TRUE);

-- ================================
-- Many-to-Many Relationship Inserts
-- ================================
INSERT INTO Workers_Inspections (worker_id, inspection_id) 
VALUES (201, 1);

INSERT INTO Hydrants_Inspections (hydrant_id, inspection_id) 
VALUES (1, 1);
