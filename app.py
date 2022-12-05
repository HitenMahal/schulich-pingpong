import sqlite3
from flask import Flask, session, render_template, request, g

from SQLDriver import *

app = Flask(__name__)

@app.route('/')
def index():
    init_db()
    initDefaultUsersAndAdmins()
    dbTest()
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'], endpoint='login')
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if loginUser(int(username), password):
            print("USERNAME:",username, "PASSWORD:",password)
            return render_template("home.html", username=username)
        else:
            return render_template("index.html", LOGIN_ERROR_MSG="Invalid username or password")
    else:
        return render_template("index.html")

@app.route('/register', methods=['GET', 'POST'], endpoint='register')
def register():
    if request.method == 'POST':
        if add_new_profile(request.form['ucid'], request.form['password'], request.form['name'], request.form['email']):
            return render_template("index.html",REGISTER_MSG="Registration successful")
        else:
            return render_template("index.html",REGISTER_MSG="Registration failed")
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

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run(debug=True)