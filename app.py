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
            return render_template("incorrectPassword.html")
    else:
        return render_template("index.html")
            
@app.route('/stats', methods=['GET', 'POST'], endpoint='stats')
def stats():
    if request.method == 'POST':
        return render_template("stats.html")
    else:
        return render_template("home.html")

@app.route('/SUBMIT_TEAMS', methods=['GET', 'POST'], endpoint='SUBMIT_TEAMS')
def SUBMIT_TEAMS():
    if request.method == 'POST':
        team_name = request.form['team_name']
        team_type = request.form['team_type']
        team_id = request.form['team_id']
        # player_ucid = request.form['player_ucid']
        if new_team(int(team_id), team_name, team_type):
            print("TEAM ID: ", team_id, "TEAM NAME: ", team_name, "TEAM TYPE: ", team_type)
            return render_template("teams.html", team_id = team_id, team_name = team_name, team_type = team_type)
    else:
        return render_template("home.html")

@app.route('/Delete_Teams', methods=['GET', 'POST'], endpoint='Delete_Teams')
def Delete_Teams():
    if request.method == 'POST':
        team_id = request.form['team_id']
        if delete_team(int(team_id)):
            print("TEAM ID: ", team_id)
            return render_template("teams.html", team_id = team_id)
    else:
        return render_template("home.html")

@app.route('/add_member', methods=['GET', 'POST'], endpoint='add_member')
def add_member():
    if request.method == 'POST':
        player_ucid = request.form['player_ucid']
        if add_team_member(player_ucid):
            print("PLAYER UCID: ", player_ucid)
            return render_template("teams.html", player_ucid = player_ucid)
    else:
        return render_template("home.html")

@app.route('/remove_member', methods=['GET', 'POST'], endpoint='remove_member')
def remove_member():
    if request.method == 'POST':
        player_ucid = request.form['player_ucid']
        if remove_team_member(player_ucid):
            print("PLAYER UCID: ", player_ucid)
            return render_template("teams.html", player_ucid = player_ucid)
    else:
        return render_template("home.html")

@app.route('/editTeams', methods=['GET', 'POST'], endpoint='editTeams')
def editTeams():
    if request.method == 'POST':
            return render_template("editTeams.html")
    else:
        return render_template("home.html")

@app.route('/teams', methods=['GET', 'POST'], endpoint='teams')
def teams():
    if request.method == 'POST':
            return render_template("teams.html")
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