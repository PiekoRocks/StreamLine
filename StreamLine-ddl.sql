-- DDL.sql - Database Schema for StreamLine Web Application

-- ================================
-- NOTE: The schema defines tables and their relationships.
-- Primary keys are set to AUTO_INCREMENT for automatic ID generation.
-- Foreign keys enforce referential integrity.
-- ================================

-- ================================
-- Regions Table
-- ================================
CREATE TABLE Regions (
    region_id INT NOT NULL AUTO_INCREMENT,
    county_name VARCHAR(255) NOT NULL,
    region_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (region_id)
);

-- ================================
-- Workers Table
-- ================================
CREATE TABLE Workers (
    worker_id INT NOT NULL AUTO_INCREMENT,
    region_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    salary DECIMAL(10,2) NOT NULL,
    assigned_date DATE NOT NULL,
    PRIMARY KEY (worker_id),
    FOREIGN KEY (region_id) REFERENCES Regions(region_id) ON DELETE CASCADE
);

-- ================================
-- Hydrants Table
-- ================================
CREATE TABLE Hydrants (
    hydrant_id INT NOT NULL AUTO_INCREMENT,
    region_id INT NOT NULL,
    flow_rate INT NOT NULL,
    is_operational TINYINT(1) NOT NULL,  -- MySQL uses TINYINT(1) for boolean values
    gps_long DECIMAL(9,6) NOT NULL,
    gps_lat DECIMAL(8,6) NOT NULL,
    PRIMARY KEY (hydrant_id),
    FOREIGN KEY (region_id) REFERENCES Regions(region_id) ON DELETE CASCADE
);

-- ================================
-- Inspections Table
-- ================================
CREATE TABLE Inspections (
    inspection_id INT NOT NULL AUTO_INCREMENT,
    inspection_date DATE NOT NULL,
    inspection_completed TINYINT(1) NOT NULL,  -- MySQL uses TINYINT(1) for boolean values
    note TEXT,
    PRIMARY KEY (inspection_id)
);

-- ================================
-- Maintenance Logs Table
-- ================================
CREATE TABLE Maintenance_Logs (
    maintenance_id INT NOT NULL AUTO_INCREMENT,
    maint_hydrant_id INT NOT NULL,
    maint_cost DECIMAL(10,2) NOT NULL,
    maint_needed TINYINT(1) NOT NULL,  -- MySQL uses TINYINT(1) for boolean values
    PRIMARY KEY (maintenance_id),
    FOREIGN KEY (maint_hydrant_id) REFERENCES Hydrants(hydrant_id) ON DELETE CASCADE
);

-- ================================
-- Many-to-Many Relationship Tables
-- ================================

-- Workers assigned to inspections
CREATE TABLE Workers_Inspections (
    worker_id INT NOT NULL,
    inspection_id INT NOT NULL,
    PRIMARY KEY (worker_id, inspection_id),
    FOREIGN KEY (worker_id) REFERENCES Workers(worker_id) ON DELETE CASCADE,
    FOREIGN KEY (inspection_id) REFERENCES Inspections(inspection_id) ON DELETE CASCADE
);

-- Hydrants assigned to inspections
CREATE TABLE Hydrants_Inspections (
    hydrant_id INT NOT NULL,
    inspection_id INT NOT NULL,
    PRIMARY KEY (hydrant_id, inspection_id),
    FOREIGN KEY (hydrant_id) REFERENCES Hydrants(hydrant_id) ON DELETE CASCADE,
    FOREIGN KEY (inspection_id) REFERENCES Inspections(inspection_id) ON DELETE CASCADE
);

-- ================================
-- Set AUTO_INCREMENT Start Values
-- ================================
ALTER TABLE Regions AUTO_INCREMENT = 101;
ALTER TABLE Workers AUTO_INCREMENT = 201;
