-- DML.sql - Data Manipulation Queries for Web Application

-- ================================
-- NOTE: The colon (:) character is used to denote variables
-- that will receive values from the backend programming language.
-- ================================

-- ================================
-- Hydrants Queries
-- ================================

-- Retrieve all hydrant info for the Manage Hydrants page
SELECT hydrant_id AS ID, Regions.region_name AS Region, flow_rate AS 'Flow Rate', 
       IF(is_operational, 'Yes', 'No') AS Operational, gps_long AS Longitude, gps_lat AS Latitude 
FROM Hydrants
JOIN Regions ON Hydrants.region_id = Regions.region_id;

-- Add a new hydrant from the Manage Hydrants page
-- NOTE: Ensure `regionInput` represents the `region_id`, not the name.
-- It may be best to implement a dropdown selection in the frontend.
INSERT INTO Hydrants (region_id, flow_rate, is_operational, gps_long, gps_lat)
VALUES (:regionInput, :flowRateInput, :isOperationalCheckboxResult, :longitudeInput, :latitudeInput);

-- Edit a hydrant already in the database from the Manage Hydrants page
UPDATE Hydrants 
SET region_id = :regionInput, flow_rate = :flowRateInput, is_operational = :isOperationalCheckboxResult, 
    gps_long = :longitudeInput, gps_lat = :latitudeInput
WHERE hydrant_id = :ID_of_selected_hydrant;

-- Delete a hydrant from the database via the Manage Hydrants page
DELETE FROM Hydrants WHERE hydrant_id = :ID_of_selected_hydrant;

-- ================================
-- Regions Queries
-- ================================

-- Retrieve all region info for the Manage Regions page
SELECT region_id AS ID, county_name AS 'County Name', region_name AS 'Region Name', division_name AS 'Division Name' 
FROM Regions;

-- Add a new region from the Manage Regions page
INSERT INTO Regions (county_name, region_name, division_name)
VALUES (:countyNameInput, :regionNameInput, :divisionNameInput);

-- Edit an existing region from the Manage Regions page
UPDATE Regions 
SET county_name = :countyNameInput, region_name = :regionNameInput, division_name = :divisionNameInput
WHERE region_id = :ID_of_selected_region;

-- Delete a region from the database via the Manage Regions page
DELETE FROM Regions WHERE region_id = :ID_of_selected_region;

-- ================================
-- Inspections Queries
-- ================================

-- Retrieve all inspection info for the Manage Inspections page
SELECT inspection_id AS ID, inspection_date AS Date, IF(inspection_completed, 'Passed', 'Failed') AS Status, note AS Notes 
FROM Inspections;

-- Add a new inspection from the Manage Inspections page
INSERT INTO Inspections (inspection_date, inspection_completed, note)
VALUES (:inspectionDateInput, :inspectionStatusOptionResult, :noteInput);

-- Edit an existing inspection from the Manage Inspections page
UPDATE Inspections 
SET inspection_date = :inspectionDateInput, inspection_completed = :inspectionStatusOptionResult, note = :noteInput
WHERE inspection_id = :ID_of_selected_inspection;

-- Delete an inspection from the database via the Manage Inspections page
DELETE FROM Inspections WHERE inspection_id = :ID_of_selected_inspection;

-- ================================
-- Workers Queries
-- ================================

-- Retrieve all workers and their assigned regions
SELECT W.worker_id, W.worker_name, R.region_name 
FROM Workers W 
JOIN Regions R ON W.region_id = R.region_id;

-- Add a new worker from the Manage Workers page
INSERT INTO Workers (region_id, worker_name, salary, assigned_date)
VALUES (:regionInput, :workerNameInput, :salaryInput, :assignedDateInput);

-- Edit an existing worker from the Manage Workers page
UPDATE Workers 
SET region_id = :regionInput, worker_name = :workerNameInput, salary = :salaryInput, assigned_date = :assignedDateInput
WHERE worker_id = :ID_of_selected_worker;

-- Delete a worker from the database via the Manage Workers page
DELETE FROM Workers WHERE worker_id = :ID_of_selected_worker;

-- ================================
-- Maintenance Queries
-- ================================

-- Retrieve all hydrants that need maintenance
SELECT H.hydrant_id, H.flow_rate, H.is_operational, M.maint_needed 
FROM Hydrants H 
JOIN Maintenance_Logs M ON H.hydrant_id = M.maint_hydrant_id 
WHERE M.maint_needed = TRUE;

-- Add a new maintenance log entry
INSERT INTO Maintenance_Logs (maint_hydrant_id, maint_cost, maint_needed)
VALUES (:hydrantIDInput, :maintenanceCostInput, :maintenanceNeededCheckbox);

-- Update maintenance status for a hydrant
UPDATE Maintenance_Logs 
SET maint_needed = :maintenanceNeededCheckbox
WHERE maint_hydrant_id = :ID_of_selected_hydrant;

-- Delete a maintenance log entry from the database
DELETE FROM Maintenance_Logs WHERE maintenance_id = :ID_of_selected_maintenance;

-- ================================
-- End of Queries
-- ================================