import sqlite3
from flask import g

def connect_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('lib/users')
    return db

def init_db():
    db = connect_db()
    cursor = db.cursor()
    # EndUser
    cursor.execute("DROP TABLE IF EXISTS EndUser")
    cursor.execute("CREATE TABLE EndUser (UCID INTEGER PRIMARY KEY, password TEXT, name TEXT, email TEXT, userType TEXT)")
    # Users
    cursor.execute("DROP TABLE IF EXISTS Users")
    cursor.execute("CREATE TABLE Users (weeklyHourLimit TEXT, UCID INTEGER, PRIMARY KEY(UCID), FOREIGN KEY (UCID) REFERENCES EndUser(Ucid))")
    # Building
    cursor.execute("DROP TABLE IF EXISTS Building")
    cursor.execute("CREATE TABLE Building (buildingName	TEXT, location TEXT, facilities TEXT, PRIMARY KEY (buildingName));")
    # Admin
    cursor.execute("DROP TABLE IF EXISTS Admins")
    cursor.execute("CREATE TABLE Admins (UCID INTEGER, BName TEXT, PRIMARY KEY (UCID, BName), FOREIGN KEY (BName) 	REFERENCES Building(buildingName), FOREIGN KEY (UCID) REFERENCES EndUser(UCID));")
    # Stats
    cursor.execute("DROP TABLE IF EXISTS Stats")
    cursor.execute("CREATE TABLE Stats (UCID INTEGER, statDistinguisher	INTEGER, mathcesWon	INTEGER, hoursPlayed INTEGER, matchesPlayed	INTEGER, PRIMARY KEY(UCID, statDistinguisher), FOREIGN KEY (UCID) REFERENCES Users (UCID));")
    # Events
    cursor.execute("DROP TABLE IF EXISTS Events")
    cursor.execute("CREATE TABLE Events(BName TEXT,EName TEXT,PRIMARY KEY(EName, BName),FOREIGN KEY(BName) REFERENCES Building(buildingName));")
    # Leaderboard
    cursor.execute("DROP TABLE IF EXISTS Leaderboard")
    cursor.execute("CREATE TABLE LeaderBoard (LName	TEXT,EName TEXT,BName TEXT,PRIMARY KEY(LName, EName, BName),FOREIGN KEY(EName)	REFERENCES eventsHappining(EName),FOREIGN KEY(BName) REFERENCES Building(buildingName));")
    # Team
    cursor.execute("DROP TABLE IF EXISTS Team")
    cursor.execute("CREATE TABLE Team(teamID INTEGER,LName TEXT,teamType TEXT,teamName	TEXT,PRIMARY KEY (teamID, LName),FOREIGN KEY (LName) REFERENCES LeaderBoard(LName));")
    # UserIsInTeam
    cursor.execute("DROP TABLE IF EXISTS User_Is_In_Team")
    cursor.execute("CREATE TABLE User_Is_In_Team(UCID INTEGER,teamID INTEGER,PRIMARY KEY(UCID, teamID),FOREIGN KEY (UCID) REFERENCES Users (UCID),FOREIGN KEY (teamID) REFERENCES Team (teamID));")
    # Game
    cursor.execute("DROP TABLE IF EXISTS Game")
    cursor.execute("CREATE TABLE Game (LName TEXT,matchID INTEGER,score	INTEGER,matchDate TEXT,PRIMARY KEY(LName, matchID),FOREIGN KEY(Lname) REFERENCES LeaderBoard(LName));")
    # Game_Player_Id
    cursor.execute("DROP TABLE IF EXISTS Game_Player_Id")
    cursor.execute("CREATE TABLE Game_Player_Id (matchID INTEGER,PUCID INTEGER,PRIMARY KEY(matchID, PUCID),FOREIGN KEY(matchID)	REFERENCES gamePlayed(matchID),FOREIGN KEY(PUCID) REFERENCES Users(UCID));")
    # Team_Player_Id
    cursor.execute("DROP TABLE IF EXISTS Team_Player_Id")
    cursor.execute("CREATE TABLE Team_Player_Id (teamID	INTEGER,PUCID INTEGER,PRIMARY KEY(teamID, PUCID),FOREIGN KEY(teamID) REFERENCES Team(teamID),FOREIGN KEY(PUCID) REFERENCES Users(UCID));")
    # Building_Tables
    cursor.execute("DROP TABLE IF EXISTS Building_Tables")
    cursor.execute("CREATE TABLE Building_Tables(BName TEXT,tableNumber INTEGER,PRIMARY KEY(BName, tableNumber),FOREIGN KEY(BName) REFERENCES building(buildingName));")
    # Schedule_Time_Slots
    cursor.execute("DROP TABLE IF EXISTS Schedule_Time_Slots")
    cursor.execute("CREATE TABLE Schedule_Time_Slots(scheduleNumber INTEGER,timeSlot INTEGER,PRIMARY KEY(scheduleNumber, timeSlot));")
    # Schedule
    cursor.execute("DROP TABLE IF EXISTS Schedule")
    cursor.execute("CREATE TABLE Schedule (tableNumber INTEGER,scheduleNumber INTEGER,PRIMARY KEY(tableNumber, scheduleNumber),FOREIGN KEY(tableNumber)	REFERENCES availableTables(tableNumber));")
    # Booking
    cursor.execute("DROP TABLE IF EXISTS Booking")
    cursor.execute("CREATE TABLE Booking (forTimeStamp TEXT,scheduleNumber INTEGER,UCID INTEGER,PRIMARY KEY(forTimeStamp, scheduleNumber, UCID),FOREIGN KEY(UCID) REFERENCES Users(UCID),FOREIGN KEY(scheduleNumber) REFERENCES schedules(scheduleNumber));")
    # Rental
    cursor.execute("DROP TABLE IF EXISTS Rental")
    cursor.execute("CREATE TABLE Rental(UCID INTEGER,rentalID INTEGER,startTime INTEGER,returnTIME INTEGER,deposit INTEGER,PRIMARY KEY(UCID,rentalID),FOREIGN KEY(UCID) REFERENCES Users(UCID));")
    # Equipment
    cursor.execute("DROP TABLE IF EXISTS Equipment")
    cursor.execute("CREATE TABLE equipment(EType TEXT,maxRentalTime INTEGER,rentalID INTEGER,BName TEXT,PRIMARY KEY(EType),FOREIGN KEY(rentalID) REFERENCES rental(rentalID),FOREIGN KEY(BName) REFERENCES building(buildingName));")
    
    cursor.close()

def initDefaultUsersAndAdmins():
    db = connect_db()
    cursor = db.cursor()
    # Default Users
    cursor.execute("INSERT INTO EndUser VALUES ( 10101011, 'password', 'John Doe', 'john.doe@ucalgary.ca', 'USER')")
    cursor.execute("INSERT INTO EndUser VALUES ( 10187026, 'pass', 'Hiten Mahalwar', 'hiten.mahalwar@ucalgary.ca', 'ADMIN')")
    cursor.close()

def dbTest():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM people")
    data = cursor.fetchall()
    cursor.close()
    return [str(x) for x in data]

def loginUser(username, password):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM ENDUSER WHERE name = '{username}' AND password = '{password}'")
    cursor.close()
    if cursor.rowcount == 1:
        return True
    else:
        return False


def add_new_profile(UCID, Password, Name, Email):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"INSERT INTO ENDUSER (UCID, password, name, email, user_type) VALUES ( {UCID} , {Password}, {Name}, {Email}, 'USER')")
    cursor.close()
    if cursor.rowcount == 1:
        return True
    else:
        return False

def delete_profile(UCID):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM ENDUSER WHERE UCID = {UCID}")
    cursor.close()

def get_user_profile(UCID):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM ENDUSER WHERE UCID = {UCID}")
    cursor.close()

def get_user_stats(UCID):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM STATS WHERE UCID = {UCID}")
    cursor.close()

def add_stats(UCID, MatchesWon, MatchesPlayed, HoursPlayed):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO STATS VALUES (UCID, stat_distinguisher, {MatchesPlayed}, {MatchesWon}, {HoursPlayed})")
    cursor.close()

def delete_stats(UCID):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM STATS WHERE UCID = {UCID}")

def new_team(team_ID, team_name, team_type):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO TEAM VALUES ({team_ID}, L_name_value, {team_name}, {team_type}")

def delete_team(team_ID):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM TEAM WHERE team_id = {team_ID}")

def get_teamMember_stats(team_ID):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT s.UCID, s.stat_distinguisher, s.matches_played, s.matches_won, s.hours_player FROM STATS as s NATURAL JOIN (SELECT UCID FROM USER_IN_TEAM WHERE team_id  = {team_ID})")

def add_team_member(ucid):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO TEAM (UCID) VALUES (UCID = {ucid})")

def remove_team_member(ucid):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM TEAM WHERE UCID = {ucid}")

def get_all_teams_with_user(ucid):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT team_id FROM TEAM WHERE UCID = {ucid}")
