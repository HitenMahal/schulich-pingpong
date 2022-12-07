import sqlite3
from flask import Flask, session, render_template, request, g
from datetime import datetime

from SQLDriver import *

app = Flask(__name__)

# GLOBAL STATIC
CurrentUser = None


# END GLOBAL STATIC

@app.route('/')
def index():
    init_db()
    initDefaultUsersAndAdmins()
    dbTest()
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'], endpoint='login')
def login():
    try:
        if request.method == 'POST':
            global CurrentUser
            username = request.form['username']
            password = request.form['password']
            result, CurrentUser = loginUser(int(username), password)
            if result:
                print("USERNAME:",username, "PASSWORD:",password)
                return render_template("home.html", name=("Hi " + CurrentUser[0][2] + "!"))
            else:
                return render_template("index.html", LOGIN_ERROR_MSG="Invalid username or password")
        else:
            return render_template("index.html")
    except Exception as e:
        return render_template("index.html", LOGIN_ERROR_MSG=str(e))


@app.route('/register', methods=['GET', 'POST'], endpoint='register')
def register():
    if request.method == 'POST':
        response = add_new_profile(request.form['ucid'], request.form['password'], request.form['name'], request.form['email'])
        if response == "SUCCESS":
            return render_template("index.html",REGISTER_MSG="Registration successful")
        elif response == "FAILURE":
            return render_template("index.html",REGISTER_MSG="Registration failed")
        elif response == "UNIQUE constraint failed: EndUser.UCID":
            return render_template("index.html",REGISTER_MSG="UCID already exists in the system, please login")
        else:
            return render_template("index.html",REGISTER_MSG=response)
    else:
        return render_template("index.html")
        
@app.route('/stats', methods=['GET', 'POST'], endpoint='stats')
def stats():
    if request.method == 'POST':
        stats = get_user_stats(1)
        matchesWon = "matches Won: " + str(stats[0][2])
        hoursPlayed = "hours Played: " + str(stats[0][3])
        matchesPlayed = "matches Played: " + str(stats[0][4])
        return render_template("stats.html", matchesWon = matchesWon, hoursPlayed = hoursPlayed, matchesPlayed = matchesPlayed)
    else:
        return render_template("home.html")

@app.route('/SUBMIT_TEAMS', methods=['GET', 'POST'], endpoint='SUBMIT_TEAMS')
def SUBMIT_TEAMS():
    if request.method == 'POST':
        team_name = request.form['team_name']
        team_type = request.form['team_type']
        # player_ucid = request.form['player_ucid']
        success, team_id = new_team(team_name, team_type)
        if success:
            print("TEAM ID: ", team_id, "TEAM NAME: ", team_name, "TEAM TYPE: ", team_type)
            return render_template("teams.html", msg="Team created successfully")
        else:
            return render_template("teams.html", msg=team_id)
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

@app.route('/newRental', methods=['GET', 'POST'], endpoint='newRental')
def newRental():
    # userUCID = getUCID()
    userUCID = 1
    paddle = request.form['numberOfPaddles']
    now = datetime.now()
    current_hour = now.strftime("%H")
    hour = int(current_hour)
    current_minute = now.strftime("%M")
    current_time = now.strftime("%H:%M")
    rentTime = request.form['rentTime']
    for i in range(int(rentTime[0])):
        if (hour < 24):
            hour += 1
        else:
            hour == 0
    returnTime = str(hour) + ":" + current_minute
    deposit = 5 * int(paddle[0])
    EType = paddle[1:]
    max_rental_time = rentTime[0]
    buildingName = request.form['BName']
    success, msg = new_rental(userUCID, current_time, returnTime, deposit)
    if success:
        if update_equipment_rental(EType, msg):
            return render_template("rent.html",rentalMsg="Rental Successful, Please pickup your rental at the ESS Office at ENE 134A")
    else:
        return render_template("rent.html",rentalMsg=msg)

@app.route('/booking', methods=['GET', 'POST'], endpoint='booking')
def booking():
    if request.method == 'POST':
        return render_template("booking.html")
    else:
        return render_template("home.html")

@app.route('/book_spot', methods=['GET', 'POST'], endpoint='book_spot')
def book_spot():
    if request.method == 'POST':
        time_slot = request.form['time_slot']
        table_ID = request.form['table_ID']
        ucid = request.form['ucid']
        schedule_ID = request.form['schedule_ID']
        success = add_time_slot(time_slot, ucid, table_ID, schedule_ID)
        if success:
            print("Time Slot: ", time_slot, "UCID: ", ucid, "Table ID: ", table_ID)
        return render_template("booking.html", msg = "Booked!")
    else:
        return render_template("home.html")

@app.route('/delete_spot', methods=['GET', 'POST'], endpoint='delete_spot')
def delete_spot():
    if request.method == 'POST':
        time_slot = request.form['time_slot']
        table_ID = request.form['table_ID']
        ucid = request.form['ucid']
        schedule_ID = request.form['schedule_ID']
        success = remove_time_slot(time_slot, ucid, table_ID, schedule_ID)
        if success:
            print("Time Slot: ", time_slot, "UCID: ", ucid, "Table ID: ", table_ID, "Schedule ID: " , schedule_ID)
        return render_template("booking.html", msg1 = "Booking Deleted")
    else:
        return render_template("home.html")
@app.route('/leaderBoards', methods=['GET', 'POST'], endpoint='leaderBoards')
def leaderBoards():
    if request.method == 'POST':
        totalMatches = []
        getAllTeamInfoResult, currentUserTeamsID = getUserTeamsID(CurrentUser[0][0])
        if getAllTeamInfoResult:
            displayLeaderboardName = ''
            displayScoreAndTime = "*"
            for x in currentUserTeamsID:
                getUserLeaderboardsResult, userLeaderboards = getUserTeamsLeaderBoard(x[0])
                if getUserLeaderboardsResult:
                    for x in userLeaderboards:
                        matches = getMatches(x[0])
                        leaderBoardMatches = 0
                        displayLeaderboardName += matches[len(totalMatches)][0] + "!"
                        for match in matches:
                            leaderBoardMatches += 1
                            displayScoreAndTime += "Scores: " + match[2] + "    Time match was played: " + match[3] + "*"
                        totalMatches.append(leaderBoardMatches)
                        displayScoreAndTime += "!"
            return render_template("leaderboards.html", displayLeaderboardName = displayLeaderboardName, displayScoreAndTime = displayScoreAndTime, 
            totalMatches = totalMatches)
    else:
        return render_template("teams.html")

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run(debug=True)