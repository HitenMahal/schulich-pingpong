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
    cursor.execute("CREATE TABLE Team(teamID INTEGER PRIMARY KEY,LName TEXT,teamType TEXT,teamName TEXT,FOREIGN KEY (LName) REFERENCES LeaderBoard(LName));")
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
    cursor.execute("CREATE TABLE Team_Player_Id (teamID	INTEGER PRIMARY KEY, PUCID INTEGER,FOREIGN KEY(teamID) REFERENCES Team(teamID),FOREIGN KEY(PUCID) REFERENCES Users(UCID));")
    # Building_Tables
    cursor.execute("DROP TABLE IF EXISTS Building_Tables")
    cursor.execute("CREATE TABLE Building_Tables(BName TEXT,tableNumber INTEGER,PRIMARY KEY(BName, tableNumber),FOREIGN KEY(BName) REFERENCES building(buildingName));")
    # Schedule_Time_Slots
    cursor.execute("DROP TABLE IF EXISTS Schedule_Time_Slots")
    cursor.execute("CREATE TABLE Schedule_Time_Slots(timeSlot INTEGER, UCID INTEGER, tableID INTEGER, scheduleNumber INTEGER,PRIMARY KEY(scheduleNumber, timeSlot));")
    # Schedule
    cursor.execute("DROP TABLE IF EXISTS Schedule")
    cursor.execute("CREATE TABLE Schedule (tableNumber INTEGER,scheduleNumber INTEGER,PRIMARY KEY(tableNumber, scheduleNumber),FOREIGN KEY(tableNumber)	REFERENCES availableTables(tableNumber));")
    # Booking
    cursor.execute("DROP TABLE IF EXISTS Booking")
    cursor.execute("CREATE TABLE Booking (forTimeStamp TEXT,scheduleNumber INTEGER,UCID INTEGER,PRIMARY KEY(forTimeStamp, scheduleNumber, UCID),FOREIGN KEY(UCID) REFERENCES Users(UCID),FOREIGN KEY(scheduleNumber) REFERENCES schedules(scheduleNumber));")
    # Rental
    cursor.execute("DROP TABLE IF EXISTS Rental")
    cursor.execute("CREATE TABLE Rental(UCID INTEGER,rentalID INTEGER PRIMARY KEY,startTime TEXT,returnTime TEXT,deposit INTEGER,FOREIGN KEY(UCID) REFERENCES Users(UCID));")
    # Equipment
    cursor.execute("DROP TABLE IF EXISTS Equipment")
    cursor.execute("CREATE TABLE Equipment(EType TEXT,maxRentalTime INTEGER,rentalID INTEGER,BName TEXT,PRIMARY KEY(EType),FOREIGN KEY(rentalID) REFERENCES rental(rentalID),FOREIGN KEY(BName) REFERENCES building(buildingName));")
    
    db.commit()
    cursor.close()

def initDefaultUsersAndAdmins():
    db = connect_db()
    cursor = db.cursor()
    # Default Users
    cursor.execute("INSERT INTO EndUser VALUES ( 1, 'pass', 'John Doe', 'john.doe@ucalgary.ca', 'USER')")
    cursor.execute("INSERT INTO Stats VALUES (1, 1, 10, 20, 30)")
    cursor.execute("INSERT INTO Leaderboard VALUES ('crazy Time board', 'crazy Event', 'The Crazy Building')")
    cursor.execute("INSERT INTO Building VALUES ('The Crazy Building', 'In a crazy Location', 'Crazy Studies')")
    cursor.execute("INSERT INTO Building VALUES ('The Amazing Building', 'In a Amazing Location', 'Amazing Studies')")
    cursor.execute("INSERT INTO Building VALUES ('The Engineering Building', 'In the best Location', 'Torture Studies')")
    print(cursor.rowcount, "INIT USER")
    cursor.execute("INSERT INTO EndUser VALUES ( 2, 'password', 'Hiten Mahalwar', 'hiten.mahalwar@ucalgary.ca', 'ADMIN')")
    print(cursor.rowcount, "INIT ADMIN")
    print("USERNAME: 1, PASSWORD: pass")
    print("USERNAME: 2, PASSWORD: password")
    db.commit()
    cursor.close()

def dbTest():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM EndUser")
    data = cursor.fetchall()
    print(data)
    cursor.close()
    data = [str(x) for x in data]
    return data

def loginUser(UCID, password):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM EndUser WHERE UCID={UCID} AND password='{password}'")
    CurrentUser = cursor.fetchall()
    if len(CurrentUser) == 1:
        cursor.close()
        return True, CurrentUser
    else:
        cursor.close()
        return False, None


def add_new_profile(UCID, Password, Name, Email):
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO EndUser VALUES ( {int(UCID)}, '{Password}', '{Name}', '{Email}', 'USER')")
        db.commit()
        print(cursor.rowcount, "NEW USER")
        if cursor.rowcount == 1:
            cursor.close()
            return "SUCCESS"
        else:
            cursor.close()
            return "FAILURE"
    except Exception as e:
        return str(e)

def delete_profile(UCID):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"DELETE FROM ENDUSER WHERE UCID = {UCID}")
    cursor.close()

def edit_profile(ucid):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"UPDATE ENDUSER SET UCID=UCID_value, name=name_value, google_email=google_email_value, user_type=user_type_value WHERE UCID= {ucid}")
    db.commit()
    cursor.close()

def get_user_profile(UCID):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM ENDUSER WHERE UCID = {UCID}")
    cursor.close()

def get_user_stats(UCID):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM STATS WHERE UCID = {UCID}")
    x = cursor.fetchall()
    cursor.close()
    return x

def add_stats(UCID, MatchesWon, MatchesPlayed, HoursPlayed):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"INSERT INTO STATS VALUES (UCID, stat_distinguisher, {MatchesPlayed}, {MatchesWon}, {HoursPlayed})")
    db.commit()
    cursor.close()

def delete_stats(UCID):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"DELETE FROM STATS WHERE UCID = {UCID}")
    db.commit()
    cursor.close()

def edit_stats(ucid):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"UPDATE STATS SET stat_distinguisher = stat_distinguisher_value, matches_played = matches_played_value, matches_won = matches_won_value, hours_played = hours_played_value WHERE UCID = {ucid}")
    db.commit()
    cursor.close()


def new_team(team_name, team_type):
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO Team (LName, teamType, teamName) VALUES ('drop-in', '{team_type}', '{team_name}')")
        db.commit()
        msg = cursor.lastrowid
        if cursor.rowcount == 1:
            cursor.close()
            return True, msg
        else:
            cursor.close()
            return False, "Failed to add to DB"
    except Exception as e:
        return False, str(e)

def delete_team(team_ID):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"DELETE FROM Team WHERE team_id = {int(team_ID)}")
    db.commit()
    if cursor.rowcount == 1:
        cursor.close()
        return True
    else:
        cursor.close()
        return False

def edit_team(team_ID):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"UPDATE TEAM SET L_name = L_name_value, team_name = team_name_value, team_type = team_type_value WHERE team_id = {team_ID}")
    db.commit()
    cursor.close()

def get_teamMember_stats(team_ID):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"SELECT s.UCID, s.stat_distinguisher, s.matches_played, s.matches_won, s.hours_player FROM STATS as s NATURAL JOIN (SELECT UCID FROM USER_IN_TEAM WHERE team_id  = {team_ID})")
    cursor.close()

def add_team_member(ucid):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"INSERT INTO TEAM (UCID) VALUES (UCID = {ucid})")
    db.commit()
    if cursor.rowcount == 1:
        cursor.close()
        return True
    else:
        cursor.close()
        return False

def remove_team_member(ucid):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"DELETE FROM TEAM WHERE UCID = {ucid}")
    db.commit()
    if cursor.rowcount == 1:
        cursor.close()
        return True
    else:
        cursor.close()
        return False

def get_all_teams_with_user(ucid):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"SELECT team_id FROM TEAM WHERE UCID = {ucid}")
    cursor.close()

def new_schedule(schedule_num, ucid):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"INSERT INTO BOOKING (SSchedule#, UCID) VALUES ( SSchedule# = {schedule_num}, UCID = {ucid})")
    db.commit()
    cursor.close()

def delete_booking(time_slot):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"DELETE FROM BOOKING WHERE for_timestamp = {time_slot}")
    db.commit()
    cursor.close()

def new_rental(ucid, start_time, return_time, deposit):
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO Rental (UCID, startTime, returnTime, deposit) VALUES ({ucid}, '{start_time}', '{return_time}', {deposit})")
        db.commit()
        msg = cursor.lastrowid
        if cursor.rowcount == 1:
            cursor.close()
            return True, msg
        else:
            cursor.close()
            return False, "Rental was not succesfull, please try again"
    except Exception as e:
        return False, str(e)
    

def edit_rental(rental_id):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"UPDATE RENTAL SET L_name = UCID = UCID_value, rental_id = rental_id_value, start_time = start_time_value, return_time = return_time_value, deposit = deposit_value WHERE rental_id= {rental_id}")
    db.commit()
    cursor.close()

def new_match(match_id, ucid, score, date):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"INSERT INTO MATCH VALUES ({match_id}, {ucid}, {score}, {date})")
    db.commit()
    cursor.close()

def cancel_match(match_id):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"DELETE FROM MATCH WHERE match_id = {match_id}")
    db.commit()
    cursor.close()

def new_leaderboard(name, event_name, building_name):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"INSERT INTO LEADERBOARD (Name, E_name, B_name) VALUES (Name = {name}, E_name = {event_name}, B_name = {building_name})")
    db.commit()
    cursor.close()

def delete_leaderboard(name):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"DELETE FROM LEADERBOARD WHERE name = {name}")
    db.commit()
    cursor.close()

def new_schedule(table_num, schedule_num):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"INSERT INTO SCHEDULE VALUES ({table_num}, {schedule_num})")
    db.commit()
    cursor.close()

def delete_schedule(table_num, schedule_num):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"DELETE FROM SCHEDULE WHERE table_num = {table_num}, schedule_num = {schedule_num}")
    db.commit()
    cursor.close()

def new_equipment(type, max_rental_time, building_name):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"INSERT INTO Equipment VALUES ({type}, {max_rental_time}, {building_name})")
    db.commit()
    if cursor.rowcount == 1:
        cursor.close()
        return True
    else:
        cursor.close()
        return False

def delete_equipment(equipment_id):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"DELETE FROM Equipment WHERE equipment_id = {equipment_id}")
    db.commit()
    cursor.close()
    
def update_equipment_rental(Etype, rentalID):
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute(f"UPDATE Equipment SET rentalID = {rentalID} WHERE EType = {Etype} AND rentalID IS NULL")
        db.commit()
        if cursor.rowcount == 1:
            cursor.close()
            return True, None
        else:
            cursor.close()
            return False, "No equipment of that type is currently available, please select a different rental"
    except Exception as e:
        return False, str(e)


def add_player_ID(match_id, player_ucid):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"INSERT INTO MATCH_PLAYER_IDS VALUES ({match_id}, {player_ucid})")
    db.commit()
    cursor.close()

def remove_player_ID(player_id, player_ucid):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"DELETE FROM MATCH_PLAYER_IDS WHERE player_id = {player_id}, p_ucid = {player_ucid}")
    db.commit()
    cursor.close()

def add_event(building_name, event_name):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"INSERT INTO EVENTS VALUES ({building_name}, {event_name})")
    db.commit()
    cursor.close()

def remove_event(building_name, event_name):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"DELETE FROM EVENTS WHERE B_name = {building_name}, E_name = {event_name}")
    db.commit()
    cursor.close()

def new_building(name, location, fac):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"INSERT INTO BUILDING (Name, Location,Facilities) VALUES (Name = {name}, Location = {location},Facilities = {fac})")
    db.commit()
    cursor.close()

def delete_building(name):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"DELETE FROM BUILDING WHERE Name = {name}")
    db.commit()
    cursor.close()   

def add_time_slot(time_slot, ucid, table_ID, schedule_ID): 
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"INSERT INTO SCHEDULE_TIME_SLOTS VALUES ({int(time_slot)}, {int(ucid)}, {int(table_ID)}, {int(schedule_ID)})")
    db.commit()
    if cursor.rowcount == 1:
        cursor.close()
        return True
    else:
        cursor.close()
        return False

def remove_time_slot(time_slot, ucid, table_ID, schedule_ID):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"DELETE FROM SCHEDULE_TIME_SLOTS WHERE time_slot = {int(time_slot)}, UCID = {int(ucid)}, ")
    db.commit()
    if cursor.rowcount == 1:
        cursor.close()
        return True
    else:
        cursor.close()
        return False

def add_table(building_name, table_num):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"INSERT INTO TABLE VALUES ({building_name}, {table_num})")
    db.commit()
    cursor.close()  

def remove_table(building_name, table_num):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"DELETE FROM TABLE WHERE b_name= {building_name}, table_num= {table_num}")
    db.commit()
    cursor.close()  