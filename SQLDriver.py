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
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("CREATE TABLE users (ucid INTEGER PRIMARY KEY, password TEXT, name TEXT, email TEXT, userType TEXT)")

    cursor.execute("DROP TABLE IF EXISTS stats")


def dbTest():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM people")
    data = cursor.fetchall()
    return [str(x) for x in data]

def loginUser(username, password):
    if username=="admin" and password=="admin":
        return True
    else:
        return False

def add_new_profile(UCID, Username, Email, Type):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"INSERT INTO ENDUSER (UCID, name, google_email, user_type) VALUES ( {UCID} , {Username}, {Email}, {Type} )")
    if cursor.rowcount == 1:
        return True
    else:
        return False

def delete_profile(UCID):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM ENDUSER WHERE UCID = {UCID}")

def get_user_profile(UCID):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM ENDUSER WHERE UCID = {UCID}")

def get_user_stats(UCID):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM STATS WHERE UCID = {UCID}")

def add_stats(UCID, MatchesWon, MatchesPlayed, HoursPlayed):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO STATS VALUES ({UCID}, stat_distinguisher, {MatchesPlayed}, {MatchesWon}, {HoursPlayed})")

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

def new_booking(schedule_num, ucid):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO BOOKING (SSchedule#, UCID) VALUES ( SSchedule# = {schedule}, UCID = {ucid})")