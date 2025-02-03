-- SQL database dump

-- Converted from PostgreSQL to standard SQL

-- Table: auth_group
CREATE TABLE auth_group (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(150) NOT NULL,
    PRIMARY KEY (id)
);

-- Table: auth_group_permissions
CREATE TABLE auth_group_permissions (
    id BIGINT NOT NULL AUTO_INCREMENT,
    group_id INT NOT NULL,
    permission_id INT NOT NULL,
    PRIMARY KEY (id)
);

-- Table: auth_permission
CREATE TABLE auth_permission (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    content_type_id INT NOT NULL,
    codename VARCHAR(100) NOT NULL,
    PRIMARY KEY (id)
);

-- Table: auth_user
CREATE TABLE auth_user (
    id INT NOT NULL AUTO_INCREMENT,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMP,
    is_superuser BOOLEAN NOT NULL,
    username VARCHAR(150) NOT NULL,
    first_name VARCHAR(150) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    email VARCHAR(254) NOT NULL,
    is_staff BOOLEAN NOT NULL,
    is_active BOOLEAN NOT NULL,
    date_joined TIMESTAMP NOT NULL,
    PRIMARY KEY (id)
);

-- Table: auth_user_groups
CREATE TABLE auth_user_groups (
    id BIGINT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    group_id INT NOT NULL,
    PRIMARY KEY (id)
);

-- Table: cities_light_city
CREATE TABLE cities_light_city (
    id INT NOT NULL AUTO_INCREMENT,
    name_ascii VARCHAR(200) NOT NULL,
    slug VARCHAR(50) NOT NULL,
    geoname_id INT,
    alternate_names TEXT,
    name VARCHAR(200) NOT NULL,
    display_name VARCHAR(200) NOT NULL,
    search_names TEXT NOT NULL,
    latitude DECIMAL(8,5),
    longitude DECIMAL(8,5),
    region_id INT,
    country_id INT NOT NULL,
    population BIGINT,
    feature_code VARCHAR(10),
    timezone VARCHAR(40),
    subregion_id INT,
    PRIMARY KEY (id)
);

-- Table: cities_light_country
CREATE TABLE cities_light_country (
    id INT NOT NULL AUTO_INCREMENT,
    name_ascii VARCHAR(200) NOT NULL,
    slug VARCHAR(50) NOT NULL,
    geoname_id INT,
    alternate_names TEXT,
    name VARCHAR(200) NOT NULL,
    code2 VARCHAR(2),
    code3 VARCHAR(3),
    continent VARCHAR(2) NOT NULL,
    tld VARCHAR(5) NOT NULL,
    phone VARCHAR(20),
    PRIMARY KEY (id)
);

-- Table: cities_light_region
CREATE TABLE cities_light_region (
    id INT NOT NULL AUTO_INCREMENT,
    name_ascii VARCHAR(200) NOT NULL,
    slug VARCHAR(50) NOT NULL,
    geoname_id INT,
    alternate_names TEXT,
    name VARCHAR(200) NOT NULL,
    display_name VARCHAR(200) NOT NULL,
    geoname_code VARCHAR(50),
    country_id INT NOT NULL,
    PRIMARY KEY (id)
);

-- Table: cities_light_subregion
CREATE TABLE cities_light_subregion (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(200) NOT NULL,
    name_ascii VARCHAR(200) NOT NULL,
    slug VARCHAR(50) NOT NULL,
    geoname_id INT,
    alternate_names TEXT,
    display_name VARCHAR(200) NOT NULL,
    geoname_code VARCHAR(50),
    country_id INT NOT NULL,
    region_id INT,
    PRIMARY KEY (id)
);

-- Additional tables and data would follow the same pattern...

-- Data for auth_group
INSERT INTO auth_group (id, name) VALUES
(1, 'MIEMBRO'),
(2, 'VISITANTE'),
(3, 'ADMINISTRADOR');

-- Data for auth_group_permissions
INSERT INTO auth_group_permissions (id, group_id, permission_id) VALUES
-- Add data here...

-- Data for auth_permission
INSERT INTO auth_permission (id, name, content_type_id, codename) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
-- Add additional data here...

-- Continue with other tables and their data...
