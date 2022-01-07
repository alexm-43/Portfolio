use covid_us; 

-- Defining database/table schema

CREATE TABLE cases_deaths (
	id INT PRIMARY KEY,
	date_updated DATE,
	state VARCHAR(25),
	fips INT,
	total_cases INT,
	total_deaths INT
);

CREATE TABLE vaccines (
	id INT PRIMARY KEY,
	date_updated DATE,
	state VARCHAR(25),
	total_vaccinations INT, --total doses administered
	doses_distributed INT, --total doses recieved by state
	people_vaccinated INT, --total people with at least 1 dose
	people_fully_vaccinated INT, --total people with at least 2 doses
	daily_vaccinations INT --number of doses administered by day
);

CREATE TABLE state_populations (
	state VARCHAR(25) PRIMARY KEY,
	population INT,
	latitude DECIMAL(8,6),
	longitude DECIMAL(9,6)
);

-- Uploading data to server

LOAD DATA INFILE '/var/lib/mysql-files/covid_by_state.csv'
	INTO TABLE cases_deaths
	FIELDS TERMINATED BY ','
	IGNORE 1 ROWS;

LOAD DATA INFILE '/var/lib/mysql-files/us_vaccinations2.csv'
	INTO TABLE vaccines
	FIELDS TERMINATED BY ','
	IGNORE 1 ROWS;

LOAD DATA INFILE '/var/lib/mysql-files/population_by_state.csv'
	INTO TABLE state_populations
	FIELDS TERMINATED BY ','
	IGNORE 1 ROWS;

--Deleting records from places outside the US

SELECT DISTINCT c.state 
FROM cases_deaths c  
WHERE c.state NOT IN (
	SELECT s.state from state_populations s
	);

SELECT DISTINCT v.state 
FROM vaccines v  
WHERE v.state NOT IN (
	SELECT s.state from state_populations s
);

UPDATE vaccines
SET state = "New York"
WHERE state = "New York State"; -- updating state name to be consistent w/ other tables

DELETE FROM cases_deaths c
WHERE c.state NOT IN (
	SELECT DISTINCT s.state 
	FROM state_populations s
);

DELETE FROM vaccines v
WHERE v.state NOT IN (
	SELECT DISTINCT s.state 
	FROM state_populations s
);

--Creating a 'totals' view for aggregate metrics

CREATE VIEW totals AS
	SELECT 
		c.state,
		population, 
		max(total_cases) AS cases, 
		max(total_deaths) AS deaths,
		max(total_vaccinations) AS vaccinations,
		max(people_vaccinated) AS people_vaccinated,
		max(people_fully_vaccinated) AS fully_vaccinated
	FROM 
		cases_deaths c
	JOIN vaccines v
		ON c.state = v.state
	JOIN state_populations s
		ON c.state = s.state
	GROUP BY c.state;








