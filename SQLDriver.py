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
