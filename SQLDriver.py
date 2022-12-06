import sqlite3
from flask import g
from DBinit import connect_db, init_db, initDefaultUsersAndAdmins

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


def new_team(team_name, team_type, ucid):
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO Team (LName, teamType, teamName) VALUES ('drop-in', '{team_type}', '{team_name}')")
        msg = cursor.lastrowid
        cursor.execute(f"INSERT INTO Team_Player_Id VALUES ({msg}, {ucid})")
        db.commit()
        if cursor.rowcount == 1:
            cursor.close()
            return True, msg
        else:
            cursor.close()
            return False, "Failed to add to DB"
    except Exception as e:
        return False, str(e)

def delete_team(team_ID):
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute(f"DELETE FROM Team_Player_Id WHERE teamID = {team_ID}")
        cursor.execute(f"DELETE FROM Team WHERE teamID = {team_ID}")
        db.commit()
        if cursor.rowcount == 1:
            cursor.close()
            return True, "Team Deleted Successfully"
        else:
            cursor.close()
            return False, "Team Deletion Failed, Please Try Again"
    except Exception as e:
        return False, str(e)

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

def add_team_member(ucid, currUcid):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"SELECT teamID FROM Team AS t, Team_Player_Id AS P WHERE ")
    cursor.execute(f"INSERT INTO Team_Player_Id VALUES ()")
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
    teams = cursor.fetchall()
    if len(teams) == 1:
        cursor.close()
        return True, teams
    else:
        cursor.close()
        return False, None

def getUserTeamsID(ucid):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"SELECT teamID FROM User_Is_In_Team WHERE UCID = {ucid}")
    teams = cursor.fetchall()
    if len(teams) == 1:
        cursor.close()
        return True, teams
    else:
        cursor.close()
        return False, None

def getUserTeamsLeaderBoard(userTeamID):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"SELECT LName FROM Team WHERE teamID = {userTeamID}")
    teams = cursor.fetchall()
    if len(teams) == 1:
        cursor.close()
        return True, teams
    else:
        cursor.close()
        return False, None

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

def getMatches(leaderboardName):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM Game WHERE LNAME = '{leaderboardName}'")
    matches = cursor.fetchall()
    cursor.close()
    return matches

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

def getLeaderboards(LeaderboardName):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM LEADERBOARD WHERE LName = '{LeaderboardName}'")
    db.commit()
    leaderboards = cursor.fetchall()
    cursor.close()
    return leaderboards

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
    cursor.execute(f"DELETE FROM SCHEDULE_TIME_SLOTS WHERE timeSlot = {int(time_slot)} AND UCID = {int(ucid)} AND tableID = {int(table_ID)} AND scheduleNumber = {int(schedule_ID)}")
    db.commit()
    cursor.close()

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