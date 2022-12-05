import sqlite3
from flask import Flask, session, render_template, request, g

from SQLDriver import *

app = Flask(__name__)

@app.route('/')
def index():
    init_db()
    data = dbTest()
    return render_template("index.html", data=data)

@app.route('/login', methods=['GET', 'POST'], endpoint='login')
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if loginUser(username, password):
            print("USERNAME:",username, "PASSWORD:",password)
            return render_template("home.html", username=username)
        else:
            return render_template("incorrectPassword.html")
    else:
        return render_template("index.html")
            
@app.route('/stats', methods=['GET', 'POST'], endpoint='stats')
def stats():
    if request.method == 'POST':
        return render_template("stats.html")
    else:
        return render_template("home.html")

@app.route('/teams', methods=['GET', 'POST'], endpoint='teams')
def teams():
    if request.method == 'POST':
        team_name = request.form['team_name']
        team_type = request.form['team_type']
        team_id = request.form['team_id']
        player_ucid = request.form['player_ucid']
        if new_team(team_id, team_name, team_type):
            print("TEAM ID: ", team_id, "TEAM NAME: ", team_name, "TEAM TYPE: ", team_type)
            return render_template("teams.html", team_id = team_id, team_name = team_name, team_type = team_type)
    else:
        return render_template("home.html")

@app.route('/rent', methods=['GET', 'POST'], endpoint='rent')
def rent():
    if request.method == 'POST':
        return render_template("rent.html")
    else:
        return render_template("home.html")

@app.route('/register', methods=['GET', 'POST'], endpoint='register')
def register():
    if request.method == 'POST':
        if registerUser(request.form['username'], request.form['password'], request.form['name'], request.form['email'], request.form['ucid']):
            return render_template("registerGood.html")
        else:
            return render_template("registerBad.html")
    else:
        return render_template("index.html")

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run(debug=True)