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

def get_user_stats(UCID):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM STATS WHERE UCID = {UCID}")
    x = cursor.fetchall()
    cursor.close()
    return x

def new_team(team_name, team_type, ucid):
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute(f"SELECT teamID FROM Team_Player_Id WHERE PUCID={ucid}")
        if len(cursor.fetchall()) > 0:
            return False, "You are already in a team, Currently only 1 team per user is allowed, Support for more teams will be coming soon!"
        cursor.execute(f"INSERT INTO Team (LName, teamType, teamName) VALUES ('Drop-in', '{team_type}', '{team_name}')")
        teamID = cursor.lastrowid
        cursor.execute(f"INSERT INTO Team_Player_Id VALUES ({teamID}, {ucid})")
        db.commit()
        if cursor.rowcount == 1:
            cursor.close()
            return True, teamID
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

def add_team_member(ucid, currUcid):
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute(f"SELECT teamID FROM Team_Player_Id WHERE PUCID={currUcid}")
        teamID = cursor.fetchone()[0]
        cursor.execute(f"INSERT INTO Team_Player_Id VALUES ({teamID}, {ucid})")
        db.commit()
        if cursor.rowcount == 1:
            cursor.close()
            return True, "Successfully Added Team Member"
        else:
            cursor.close()
            return False, "Failed to add Team Member"
    except Exception as e:
        return False, str(e)

def remove_team_member(ucid):
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute(f"DELETE FROM Team_Player_Id WHERE PUCID = {ucid}")
        db.commit()
        if cursor.rowcount == 1:
            cursor.close()
            return True, "Successfully Removed Team Member"
        else:
            cursor.close()
            return False, "Failed to Remove Team Member"
    except Exception as e:
        return False, str(e)

def get_all_teams_with_user(ucid):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"SELECT teamId FROM Team_Player_Id WHERE PUCID = {ucid}")
    teams = cursor.fetchall()
    teams = [int(x[0]) for x in teams]
    if teams==[]:
        cursor.close()
        return None
    output = []
    for team in teams:
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM Team WHERE teamID = {team}")
        output.append(cursor.fetchone())
    cursor.close()
    return output

def getUserTeamsID(ucid):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"SELECT teamID FROM Team_Player_Id WHERE PUCID = {ucid}")
    teams = cursor.fetchall()
    if len(teams) > 0:
        cursor.close()
        return True, teams
    else:
        cursor.close()
        return False, None

def getTeamFromLeaderboard(leaderboardName):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM Team WHERE LName = '{leaderboardName}'")
    teams = cursor.fetchall()
    if len(teams) > 0:
        cursor.close()
        return True, teams
    else:
        cursor.close()
        return False, None

def getUserTeamsLeaderBoard(userTeamID):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM Team WHERE teamID = {userTeamID}")
    teams = cursor.fetchall()
    if len(teams) == 1:
        cursor.close()
        return True, teams
    else:
        cursor.close()
        return False, None

def editTeamLName(leaderboardName):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"UPDATE Team SET LName = 'drop-in' WHERE LName = '{leaderboardName}'")
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
    
def cancel_rental(ucid):
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute(f"DELETE FROM Rental WHERE UCID = {ucid}")
        db.commit()
        if cursor.rowcount == 1:
            cursor.close()
            return True, "Rental Cancelled"
        else:
            cursor.close()
            return False, "Rental was not cancelled, please try again"
    except Exception as e:
        return False, str(e)

def new_Game(leaderboardName, scoreONE, scoreTWO, matchDATE):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"INSERT INTO Game (LName, score1, score2, matchDate) VALUES ('{leaderboardName}', {scoreONE}, {scoreTWO}, '{matchDATE}')")
    db.commit()
    cursor.close()

def getMatches(leaderboardName):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM Game WHERE LNAME = '{leaderboardName}'")
    matches = cursor.fetchall()
    if len(matches) > 0:
        cursor.close()
        return matches
    else:
        cursor.close()
        return None

def cancel_Game(match_id):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"DELETE FROM Game WHERE matchID = {match_id}")
    db.commit()
    cursor.close()

def new_leaderboard(name, event_name, building_name):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"INSERT INTO Leaderboard (Name, E_name, B_name) VALUES (Name = {name}, E_name = {event_name}, B_name = {building_name})")
    db.commit()
    cursor.close()

def getAllLeaderboards():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Leaderboard")
    db.commit()
    leaderboards = cursor.fetchall()
    if len(leaderboards) > 0 :
        cursor.close()
        return True, leaderboards
    else:
        cursor.close()
        return False, None

def delete_leaderboard(name):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"DELETE FROM Leaderboard WHERE LName = '{name}'")
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

def add_time_slot(time_slot, ucid, table_ID, schedule_ID): 
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO SCHEDULE_TIME_SLOTS VALUES ({int(time_slot)}, {int(ucid)}, {int(table_ID)}, {int(schedule_ID)})")
        db.commit()
        if cursor.rowcount == 1:
            cursor.close()
            return True, "Succesfully Booked"
        else:
            cursor.close()
            return False, "Time slot is unavailable"
    except Exception as e:
        return False, str(e)

def remove_time_slot(time_slot, ucid, table_ID, schedule_ID):
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute(f"DELETE FROM SCHEDULE_TIME_SLOTS WHERE timeSlot = {int(time_slot)} AND UCID = {int(ucid)} AND tableID = {int(table_ID)} AND scheduleNumber = {int(schedule_ID)}")
        db.commit()
        if cursor.rowcount == 1:
            cursor.close()
            return True, "Successfully Cancelled Booking"
        else:
            cursor.close()
            return False, "Unable to cancel that bookings"
    except Exception as e:
        return False, str(e)