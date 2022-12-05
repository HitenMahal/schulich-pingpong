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

