INSERT INTO Countries (countryName, globalRegion, population, GDP)
VALUES
	('United States', 'North America', 3310002651, 21.4),
	('China', 'Asia', 1439323776, 14.3),
    ('India', 'Asia', 1380004385, 2.8),
    ('Brazil', 'South America', 212559417, 1.4),
    ('Russia', 'Asia', 145934462, 1.4);

INSERT INTO Consumers (municipality, population, annualConsumption)
VALUES 
	('New York City', 8336817, 180000),
	('Shanghai', 24281000, 220000),
    ('Mumbai', 20411274, 120000),
    ('Sao Paulo', 12252023, 160000),
    ('Moscow', 12537954, 100000);

INSERT INTO Energy_Types (energyName, emissionsRate, deathRate)
VALUES 
	('Solar', 45, 0.01),
	('Wind', 10, 0.005),
    ('Coal', 100, 0.02),
    ('Nuclear', 15, 0.002),
    ('Hydro', 5, 0.001); 

INSERT INTO Providers (providerName, orgType)
VALUES
	('ABC Energy', 'Public'),
    ('XYZ Power', 'Private'),
    ('PowerCo', 'Public'),
    ('EcoEnergy', 'Private'),
    ('GreenPower', 'Cooperative');