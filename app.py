import sqlite3
from flask import Flask, session, render_template, request, g

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Hello World!</h1>"

def connect_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('database.db')
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run()