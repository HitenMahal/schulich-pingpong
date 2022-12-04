import sqlite3
from flask import Flask, session, render_template, request, g

from SQLDriver import connect_db

app = Flask(__name__)

@app.route('/')
def index():
    data = connect_db()
    return str(data)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run()