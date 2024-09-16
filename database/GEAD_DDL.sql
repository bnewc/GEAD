DROP TABLE IF EXISTS Countries, Consumers, Energy_Types, Providers, Provider_Energy_Types, National_Operations, Energy_Provisions;

-- Countries Table

CREATE TABLE `Countries` (
	`countryID` int NOT NULL auto_increment,
	`countryName` varchar(50) NOT NULL,
	`globalRegion` varchar(45) NOT NULL,
	`population` bigint(12) NOT NULL,
	`gdp` decimal(10,3),
	PRIMARY KEY (`countryID`),
    UNIQUE(countryName)
);

-- Consumers Table

CREATE TABLE `Consumers` (
	`consumerID` int NOT NULL auto_increment,
	`municipality` varchar(100) NOT NULL,
	`population` int(11),
	`annualConsumption` int(11),
	PRIMARY KEY (`consumerID`),
);

-- Energy_Types Table

CREATE TABLE `Energy_Types` (
	`energyTypeID` int(11) NOT NULL auto_increment,
	`energyName` varchar(45) NOT NULL,
	`emissionsRate` int(11),
	`deathRate` decimal(10,4),
	PRIMARY KEY (`energyTypeID`),
    UNIQUE(energyName)
);

-- Providers Table

CREATE TABLE `Providers` (
	`providerID` int(11) NOT NULL auto_increment,
	`providerName` varchar(45) NOT NULL,
	`orgType` varchar(45) NOT NULL,
	PRIMARY KEY (`providerID`),
    UNIQUE(providerName)
);

-- Provider_Energy_Types Insersection Table

CREATE TABLE `Provider_Energy_Types` (
	`providerID` int NOT NULL,
	`energyTypeID` int NOT NULL,
	FOREIGN KEY (`providerID`) REFERENCES Providers(providerID)
		ON DELETE CASCADE,
	FOREIGN KEY (`energyTypeID`) REFERENCES Energy_Types(energyTypeID)
		ON DELETE CASCADE,
	UNIQUE(providerID, energyTypeID)
);

-- National_Operations Intersection Table

CREATE TABLE `National_Operations` (
	`providerID` int NOT NULL,
    `countryID` int,
    FOREIGN KEY (`providerID`) REFERENCES Providers(providerID)
		ON DELETE CASCADE,
	FOREIGN KEY (`countryID`) REFERENCES Countries(countryID)
		ON DELETE SET NULL,
	UNIQUE(providerID, countryID)
);

-- Energy_Provisions Intersection Table

CREATE TABLE `Energy_Provisions` (
	`providerID` int NOT NULL,
	`consumerID` int NOT NULL,
    `energyTypeID` int NOT NULL,
    FOREIGN KEY (`providerID`) REFERENCES Providers(providerID)
		ON DELETE CASCADE,
	FOREIGN KEY (`consumerID`) REFERENCES Consumers(consumerID)
		ON DELETE CASCADE,
	FOREIGN KEY (`energyTypeID`) REFERENCES Energy_Types(energyTypeID)
		ON DELETE CASCADE,
	UNIQUE(providerID, consumerID, energyTypeID)
);
