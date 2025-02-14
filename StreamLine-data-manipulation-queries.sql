-- colon : character used to denote the variables that will have data from the backend programming language.

-- Hydrants Queries
-- get all hydrant info for the Manage Hydrants page
SELECT hydrant_id AS ID, Regions.region_name AS Region, flow_rate AS 'Flow Rate', if(is_operational, 'Yes', 'No') AS Operational, gps_long AS Longitude, gps_lat AS Latitude FROM Hydrants
JOIN Regions ON Hydrants.region_id = Regions.region_id

-- add a new hydrant from the Manage Hydrants page
INSERT INTO Hydrants (region_id, flow_rate, is_operational, gps_long, gps_lat)
VALUES (:regionInput, :flowRateInput, :isOperationalCheckboxResult, :longitudeInput, :latitudeInput)
-- Is region input the region id? or is it the name? should this be a dropdown like in the bsg sample? (also a concern for update query below)

-- edit a hydrant already in the database from the Manage Hydrants page
UPDATE Hydrants SET region_id = :regionInput, flow_rate = :flowRateInput, is_operational = :isOperationalCheckboxResult, gps_long = :longitudeInput, gps_lat = :latitudeInput
WHERE hydrant_id = :ID_of_selected_hydrant

-- delete a hydrant in the database from the Manage Hydrants page
DELETE FROM Hydrants WHERE hydrant_id = :ID_of_selected_hydrant

-- Regions Queries
-- get all region info for the Manage Regions page
SELECT region_id AS ID, county_name AS 'County Name', region_name AS 'Region Name', division_name AS 'Division Name' FROM Regions

-- add a new region from the Manage Regions page
INSERT INTO Regions (county_name, region_name, division_name)
VALUES (:countyNameInput, :regionNameInput, :divisionNameInput)

-- edit a region already in the database from the Manage Regions page
UPDATE Regions SET county_name = :countyNameInput, region_name = :regionNameInput, division_name = :divisionNameInput
WHERE region_id = :ID_of_selected_region

-- delete a region in the database from the Manage Regions page
DELETE FROM Regions WHERE region_id = :ID_of_selected_region

-- Inspections Queries
-- get all inspection info for the Manage Inspections page
SELECT inspection_id AS ID, inspection_date AS Date, if(inspection_status, 'Passed', 'Failed') AS Status, note AS Notes FROM Inspections

-- add a new inspection from the Manage Inspections page
INSERT INTO Inspections (inspection_date, inspection_status, note)
VALUES (:inspectionDateInput, :inspectionStatusOptionResult, :noteInput)

-- edit an inspection already in the database from the Manage Inspections page
UPDATE Inspections SET inspection_date = :inspectionDateInput, inspection_status = :inspectionStatusOptionResult, note = :noteInput
WHERE inspection_id = :ID_of_selected_inspection

-- delete an inspection in the database from the Manage Inspections page
DELETE FROM Inspections WHERE inspection_id = :ID_of_selected_inspection

--Additional queries are WIP
