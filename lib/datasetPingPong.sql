DROP DATABASE IF EXISTS PingPongApp;
CREATE DATABASE PingPongApp;

USE PingPongApp;

CREATE TABLE EndUser (
	UCID						int unsigned NOT NULL,
    FullName					VARCHAR(150) NOT NULL,
    GoogleEmail					VARCHAR(150) NOT NULL,
    userType					BOOL NOT NULL,
	PRIMARY KEY (UCID)
);

CREATE TABLE User (
	weeklyHourLimit				int unsigned NOT NULL,
    UCID						int unsigned NOT NULL,
	FOREIGN KEY (UCID)			REFERENCES EndUser(UCID)
);

CREATE TABLE Admin (
	UCID						int unsigned NOT NULL,
    BName						VARCHAR(150) NOT NULL,
	FOREIGN KEY (BName) 		REFERENCES Building(Name),
	FOREIGN KEY (UCID) 			REFERENCES EndUser(UCID)
);

CREATE TABLE Stats (
	statDistinguisher			int unsigned NOT NULL,
    mathcesWon					int unsigned NOT NULL,
    hoursPlayed					int unsigned NOT NULL,
    matchesPlayed				int unsigned NOT NULL,
    PRIMARY KEY (statDistinguisher),
    FOREIGN KEY (UCID)			REFERENCES User (UCID)
);

CREATE TABLE Team (
	
);