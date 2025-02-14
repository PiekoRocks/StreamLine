-- DDL.sql - Data Definition Language (Schema Creation and Sample Data Insertion)

-- ================================
-- Create Regions Table
-- Stores geographical regions where hydrants are located
-- ================================
CREATE TABLE Regions (
    region_id INT AUTO_INCREMENT PRIMARY KEY,
    county_name VARCHAR(255) NOT NULL,
    region_name VARCHAR(255) NOT NULL
);

-- ================================
-- Create Hydrants Table
-- Stores details of fire hydrants, linked to Regions
-- ================================
CREATE TABLE Hydrants (
    hydrant_id INT AUTO_INCREMENT PRIMARY KEY,
    region_id INT NOT NULL,
    flow_rate INT,
    is_operational BOOLEAN NOT NULL,
    gps_long DECIMAL(9,6) NOT NULL,
    gps_lat DECIMAL(8,6) NOT NULL,
    FOREIGN KEY (region_id) REFERENCES Regions(region_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- ================================
-- Create Inspections Table
-- Stores inspection records of hydrants
-- ================================
CREATE TABLE Inspections (
    inspection_id INT AUTO_INCREMENT PRIMARY KEY,
    inspection_date DATE NOT NULL,
    inspection_completed BOOLEAN NOT NULL,
    note TEXT
);

-- ================================
-- Create Workers Table
-- Stores worker details, linked to Regions
-- ================================
CREATE TABLE Workers (
    worker_id INT AUTO_INCREMENT PRIMARY KEY,
    region_id INT NOT NULL,
    worker_name VARCHAR(100) NOT NULL,
    salary DECIMAL(10,2) NOT NULL,
    assigned_date DATE NOT NULL,
    FOREIGN KEY (region_id) REFERENCES Regions(region_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- ================================
-- Create Maintenance Logs Table
-- Stores maintenance records for hydrants
-- ================================
CREATE TABLE Maintenance_Logs (
    maintenance_id INT AUTO_INCREMENT PRIMARY KEY,
    maint_hydrant_id INT NOT NULL,
    maint_cost DECIMAL(10,2) NOT NULL,
    maint_needed BOOLEAN NOT NULL,
    FOREIGN KEY (maint_hydrant_id) REFERENCES Hydrants(hydrant_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- ================================
-- Create Intersection Table: Workers_Inspections
-- Links workers to inspections (Many-to-Many Relationship)
-- ================================
CREATE TABLE Workers_Inspections (
    worker_id INT NOT NULL,
    inspection_id INT NOT NULL,
    PRIMARY KEY (worker_id, inspection_id),
    FOREIGN KEY (worker_id) REFERENCES Workers(worker_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (inspection_id) REFERENCES Inspections(inspection_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- ================================
-- Create Intersection Table: Hydrants_Inspections
-- Links hydrants to inspections (Many-to-Many Relationship)
-- ================================
CREATE TABLE Hydrants_Inspections (
    inspection_hydrant_id INT NOT NULL,
    inspection_id INT NOT NULL,
    PRIMARY KEY (inspection_hydrant_id, inspection_id),
    FOREIGN KEY (inspection_hydrant_id) REFERENCES Hydrants(hydrant_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (inspection_id) REFERENCES Inspections(inspection_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- ================================
-- Insert Sample Data
-- Populates tables with initial data for testing
-- ================================

-- Insert sample data into Regions Table
INSERT INTO Regions (county_name, region_name) VALUES
('Benton', 'Downtown'),
('Linn', 'Riverside'),
('Deschutes', 'High Desert'),
('Clatsop', 'North Coast'),
('Lane', 'South Valley');

-- Insert sample data into Hydrants Table
INSERT INTO Hydrants (region_id, flow_rate, is_operational, gps_long, gps_lat) VALUES
(1, 1500, TRUE, 40.712776, -74.005974),
(2, 500, TRUE, 34.052235, -118.243683),
(3, 500, FALSE, 51.507351, -0.127758),
(4, 1000, TRUE, -33.868820, 151.209290),
(5, 500, FALSE, 48.856613, 2.352222);

-- Insert sample data into Inspections Table
INSERT INTO Inspections (inspection_date, inspection_completed, note) VALUES
('2025-02-01', TRUE, 'Minor damage'),
('2025-01-15', FALSE, 'Major repair needed'),
('2024-12-20', TRUE, 'Passed inspection'),
('2025-01-25', TRUE, 'Minor leak observed'),
('2024-11-30', FALSE, 'Needs replacement');

-- Insert sample data into Workers Table
INSERT INTO Workers (region_id, worker_name, salary, assigned_date) VALUES
(1, 'John Smith', 50000, '2024-12-01'),
(2, 'Jane Doe', 55000, '2024-11-15'),
(3, 'Troy Diaz', 48000, '2024-09-10'),
(4, 'Adam Danielson', 52000, '2024-10-05'),
(5, 'Nico Johnson', 51000, '2024-08-15');

-- Insert sample data into Maintenance Logs Table
INSERT INTO Maintenance_Logs (maint_hydrant_id, maint_cost, maint_needed) VALUES
(1, 150, TRUE),
(2, 120, TRUE),
(3, 200, TRUE),
(4, 180, TRUE),
(5, 170, FALSE);

-- Insert sample data into Workers_Inspections Table
INSERT INTO Workers_Inspections (worker_id, inspection_id) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5);

-- Insert sample data into Hydrants_Inspections Table
INSERT INTO Hydrants_Inspections (inspection_hydrant_id, inspection_id) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5);
