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

def edit_profile(ucid):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("UPDATE ENDUSER SET UCID=UCID_value, name=name_value, google_email=google_email_value, user_type=user_type_value WHERE UCID= {ucid}")
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
    cursor.close()

def edit_stats(ucid):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("UPDATE STATS SET stat_distinguisher = stat_distinguisher_value, matches_played = matches_played_value, matches_won = matches_won_value, hours_played = hours_played_value WHERE UCID = {UCID}")
    cursor.close()


def new_team(team_ID, team_name, team_type):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO TEAM VALUES ({team_ID}, L_name_value, {team_name}, {team_type}")
    cursor.close()

def delete_team(team_ID):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM TEAM WHERE team_id = {team_ID}")
    cursor.close()

def edit_team(team_ID):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("UPDATE TEAM SET L_name = L_name_value, team_name = team_name_value, team_type = team_type_value WHERE team_id = {team_ID}")
    cursor.close()

def get_teamMember_stats(team_ID):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT s.UCID, s.stat_distinguisher, s.matches_played, s.matches_won, s.hours_player FROM STATS as s NATURAL JOIN (SELECT UCID FROM USER_IN_TEAM WHERE team_id  = {team_ID})")
    cursor.close()

def add_team_member(ucid):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO TEAM (UCID) VALUES (UCID = {ucid})")
    cursor.close()

def remove_team_member(ucid):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM TEAM WHERE UCID = {ucid}")
    cursor.close()

def get_all_teams_with_user(ucid):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT team_id FROM TEAM WHERE UCID = {ucid}")
    cursor.close()

def new_booking(schedule_num, ucid):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO BOOKING (SSchedule#, UCID) VALUES ( SSchedule# = {schedule}, UCID = {ucid})")
    cursor.close()

def delete_booking(time_slot):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM BOOKING WHERE for_timestamp = {time_slot}")
    cursor.close()

def new_rental(ucid, rental_id, start_time, return_time, deposit):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO RENTAL VALUES ({ucid}, {rental_id}, {start_time}, {return_time}, {deposit})")
    cursor.close()

def edit_rental(rental_id):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("UPDATE RENTAL SET L_name = UCID = UCID_value, rental_id = rental_id_value, start_time = start_time_value, return_time = return_time_value, deposit = deposit_value WHERE rental_id= {rental_id}")
    cursor.close()

def new_match(match_id, ucid, score, date):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO MATCH VALUES ({match_id}, {ucid}, {score}, {date})")
    cursor.close()

def cancel_match(match_id):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM MATCH WHERE match_id = {match_id}")
    cursor.close()

def new_leaderboard(name, event_name, building_name):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO LEADERBOARD (Name, E_name, B_name) VALUES (Name = {name}, E_name = {event_name}, B_name = {building_name})")
    cursor.close()

def delete_leaderboard(name):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM LEADERBOARD WHERE name = {name}")
    cursor.close()

def new_schedule(table_num, schedule_num):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO SCHEDULE VALUES ({table_num}, {schedule_num})")
    cursor.close()

def delete_schedule(table_num, schedule_num):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM SCHEDULE WHERE table_num = {table_num}, schedule_num = {schedule_num}")
    cursor.close()

def new_equipment(type, max_rental_time, building_name):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO EQUIPMENT VALUES ({type}, {max_rental_time}, {building_name})")
    cursor.close()

def delete_equipment(equipment_id):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM EQUIPMENT WHERE equipment_id = {equipment_id}")
    cursor.close()

def add_player_ID(match_id, player_ucid):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO MATCH_PLAYER_IDS VALUES ({match_id}, {player_ucid})")
    cursor.close()

def remove_player_ID(player_id, player_ucid):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM MATCH_PLAYER_IDS WHERE player_id = {player_id}, p_ucid = {player_ucid}")
    cursor.close()

def add_event(building_name, event_name):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO EVENTS VALUES ({building_name}, {event_name})")
    cursor.close()

def remove_event(building_name, event_name):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM EVENTS WHERE B_name = {building_name}, E_name = {event_name}")
    cursor.close()

def new_building(name, location, fac):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO BUILDING (Name, Location,Facilities) VALUES (Name = {name}, Location = {location},Facilities = {fac})")
    cursor.close()

def delete_building(name):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM BUILDING WHERE Name = {name}")
    cursor.close()   

def add_time_slot(schedule_num, time_slot): 
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO SCHEDULE_TIME_SLOTS VALUES ({schedule_num}, {time_slot})")
    cursor.close()   

def remove_time_slot(schedule_num, time_slot):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM SCHEDULE_TIME_SLOTS WHERE schedule_num = {schedule_num}, time_slot = {time_slot}")
    cursor.close()  

def add_table(building_name, table_num):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO TABLE VALUES ({building_name}, {table_num})")
    cursor.close()  

def remove_table(building_name, table_num):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM TABLE WHERE b_name= {building_name}, table_num= {table_num}")
    cursor.close()  