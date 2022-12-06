import sqlite3
from flask import g

def connect_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('lib/SPP.db')
    return db

def init_db():
    db = connect_db()
    cursor = db.cursor()
    # EndUser
    cursor.execute("DROP TABLE IF EXISTS EndUser")
    cursor.execute("""
    CREATE TABLE EndUser (
        UCID INTEGER PRIMARY KEY, 
        password TEXT, 
        name TEXT, 
        email TEXT, 
        userType TEXT
    )""")
    # Users
    cursor.execute("DROP TABLE IF EXISTS Users")
    cursor.execute("""
    CREATE TABLE Users (
        weeklyHourLimit TEXT, 
        UCID INTEGER, 
        PRIMARY KEY(UCID), 
        FOREIGN KEY (UCID) REFERENCES EndUser(Ucid)
    )""")
    # Building
    cursor.execute("DROP TABLE IF EXISTS Building")
    cursor.execute("""
    CREATE TABLE Building (
        buildingName TEXT PRIMARY KEY, 
        location TEXT, 
        facilities TEXT
    )""")
    # Admin
    cursor.execute("DROP TABLE IF EXISTS Admins")
    cursor.execute("""
    CREATE TABLE Admins (
        UCID INTEGER, 
        BName TEXT, 
        PRIMARY KEY (UCID, BName), 
        FOREIGN KEY (BName) REFERENCES Building(buildingName), 
        FOREIGN KEY (UCID) REFERENCES EndUser(UCID)
    )""")
    # Stats
    cursor.execute("DROP TABLE IF EXISTS Stats")
    cursor.execute("""
    CREATE TABLE Stats (
        UCID INTEGER, 
        statDistinguisher INTEGER, 
        mathcesWon	INTEGER, 
        hoursPlayed INTEGER, 
        matchesPlayed	INTEGER, 
        PRIMARY KEY(UCID, statDistinguisher), 
        FOREIGN KEY (UCID) REFERENCES Users (UCID)
    );""")
    # Events
    cursor.execute("DROP TABLE IF EXISTS Events")
    cursor.execute("""
    CREATE TABLE Events(
        BName TEXT,
        EName TEXT,
        PRIMARY KEY(EName, BName),
        FOREIGN KEY(BName) REFERENCES Building(buildingName)
    );""")
    # Leaderboard
    cursor.execute("DROP TABLE IF EXISTS Leaderboard")
    cursor.execute("""
    CREATE TABLE LeaderBoard (
        LName TEXT,
        EName TEXT,
        BName TEXT,
        PRIMARY KEY(LName, EName, BName),
        FOREIGN KEY(EName) REFERENCES eventsHappining(EName),
        FOREIGN KEY(BName) REFERENCES Building(buildingName)
    );""")
    # Team
    cursor.execute("DROP TABLE IF EXISTS Team")
    cursor.execute("""
    CREATE TABLE Team(
        teamID INTEGER PRIMARY KEY,
        LName TEXT,
        teamType TEXT,
        teamName TEXT,
        FOREIGN KEY (LName) REFERENCES LeaderBoard(LName)
    );""")
    # Game
    cursor.execute("DROP TABLE IF EXISTS Game")
    cursor.execute("""
    CREATE TABLE Game (
        LName TEXT,
        matchID INTEGER,
        score Text,
        matchDate TEXT,
        PRIMARY KEY(LName, matchID),
        FOREIGN KEY(Lname) REFERENCES LeaderBoard(LName)
    );""")
    # Game_Player_Id
    cursor.execute("DROP TABLE IF EXISTS Game_Player_Id")
    cursor.execute("""
    CREATE TABLE Game_Player_Id (
        matchID INTEGER,
        PUCID INTEGER,
        PRIMARY KEY(matchID, PUCID),
        FOREIGN KEY(matchID) REFERENCES gamePlayed(matchID),
        FOREIGN KEY(PUCID) REFERENCES Users(UCID)
    );""")
    # Team_Player_Id
    cursor.execute("DROP TABLE IF EXISTS Team_Player_Id")
    cursor.execute("""
    CREATE TABLE Team_Player_Id (
        teamID INTEGER PRIMARY KEY, 
        PUCID INTEGER,
        FOREIGN KEY(teamID) REFERENCES Team(teamID),
        FOREIGN KEY(PUCID) REFERENCES Users(UCID)
    );""")
    # Building_Tables
    cursor.execute("DROP TABLE IF EXISTS Building_Tables")
    cursor.execute("""
    CREATE TABLE Building_Tables(
        BName TEXT,
        tableNumber INTEGER,
        PRIMARY KEY(BName, tableNumber),
        FOREIGN KEY(BName) REFERENCES building(buildingName)
    );""")
    # Schedule_Time_Slots
    cursor.execute("DROP TABLE IF EXISTS Schedule_Time_Slots")
    cursor.execute("""
    CREATE TABLE Schedule_Time_Slots(
        timeSlot INTEGER, 
        UCID INTEGER, 
        tableID INTEGER, 
        scheduleNumber INTEGER,
        PRIMARY KEY(scheduleNumber, timeSlot)
    );""")
    # Schedule
    cursor.execute("DROP TABLE IF EXISTS Schedule")
    cursor.execute("""
    CREATE TABLE Schedule (
        tableNumber INTEGER,
        scheduleNumber INTEGER,
        PRIMARY KEY(tableNumber, scheduleNumber),
        FOREIGN KEY(tableNumber) REFERENCES availableTables(tableNumber)
    );""")
    # Booking
    cursor.execute("DROP TABLE IF EXISTS Booking")
    cursor.execute("""
    CREATE TABLE Booking (
        forTimeStamp TEXT,
        scheduleNumber INTEGER,
        UCID INTEGER,
        PRIMARY KEY(forTimeStamp, scheduleNumber, UCID),
        FOREIGN KEY(UCID) REFERENCES Users(UCID),
        FOREIGN KEY(scheduleNumber) REFERENCES schedules(scheduleNumber)
    );""")
    # Rental
    cursor.execute("DROP TABLE IF EXISTS Rental")
    cursor.execute("""
    CREATE TABLE Rental(
        UCID INTEGER,
        rentalID INTEGER PRIMARY KEY,
        startTime TEXT,
        returnTime TEXT,
        deposit INTEGER,FOREIGN KEY(UCID) REFERENCES Users(UCID)
    );""")
    # Equipment
    cursor.execute("DROP TABLE IF EXISTS Equipment")
    cursor.execute("""
    CREATE TABLE Equipment(
        EType TEXT,
        maxRentalTime INTEGER,
        rentalID INTEGER,
        BName TEXT,
        PRIMARY KEY(EType),
        FOREIGN KEY(rentalID) REFERENCES rental(rentalID),
        FOREIGN KEY(BName) REFERENCES building(buildingName)
    );""")
    
    db.commit()
    cursor.close()

def initDefaultUsersAndAdmins():
    db = connect_db()
    cursor = db.cursor()
    # Default Users
    cursor.execute("INSERT INTO EndUser VALUES ( 1, 'pass', 'John Doe', 'john.doe@ucalgary.ca', 'USER')")
    print(cursor.rowcount, "INIT USER")
    cursor.execute("INSERT INTO EndUser VALUES ( 2, 'password', 'Hiten Mahalwar', 'hiten.mahalwar@ucalgary.ca', 'ADMIN')")
    print(cursor.rowcount, "INIT ADMIN")
    # Give John Doe Stats
    cursor.execute("INSERT INTO Stats VALUES (1, 1, 10, 20, 30)")
    cursor.execute("INSERT INTO Team VALUES (1, 'Engineering Drop-In', 'SINGLES', 'Pong Pros')")
    cursor.execute("INSERT INTO Team_Player_Id VALUES (1, 1)")
    cursor.execute("INSERT INTO Game VALUES ('Engineering Drop-In', 1234, 'Crazy people: 14      Sane people: 21', '2013,02,10')")
    cursor.execute("INSERT INTO Game VALUES ('Engineering Drop-In', 4321, 'Crazy people: 21      Sane people: 14', '2013,02,10')")
    cursor.execute("INSERT INTO Leaderboard VALUES ('crazy Time board', 'crazy Event', 'The Crazy Building')")
    cursor.execute("INSERT INTO Building VALUES ('The Crazy Building', 'In a crazy Location', 'Crazy Studies')")
    cursor.execute("INSERT INTO Building VALUES ('The Amazing Building', 'In a Amazing Location', 'Amazing Studies')")
    cursor.execute("INSERT INTO Building VALUES ('The Engineering Building', 'In the best Location', 'Torture Studies')")

    print("USERNAME: 1, PASSWORD: pass")
    print("USERNAME: 2, PASSWORD: password")
    db.commit()
    cursor.close()
