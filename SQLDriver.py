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
    return cursor.fetchall()

def add_new_profile(UCID, Username, Email, Type):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(f"INSERT INTO ENDUSER (UCID, name, google_email, user_type) VALUES ( {UCID} , {Username}, {Email}, {Type} )")

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
    cursor.execute("INSERT INTO STATS VALUES (UCID, stat_distinguisher, {MatchesPlayed}, {MatchesWon}, {HoursPlayed})")

def delete_stats(UCID):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO STATS VALUES (UCID, stat_distinguisher, {MatchesPlayed}, {MatchesWon}, {HoursPlayed})")
