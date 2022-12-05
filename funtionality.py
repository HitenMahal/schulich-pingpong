import SQLDriver
class start:

    account_status = input("Login or new account or delete account\n")

    if account_status == 'login':

        validUser = 0 # starts with user info is incorrect

        while validUser == 0:

            username = input("Enter Username: ")

            password = input("Enter Password: ")

            ucid = input("Enter UCID: ")

            SQLDriver.get_user_profile(username, password, ucid) #login start
            # Returns true (1) if user info is correct, returns false (0) if info is incorrect

            if 1:

                validUser = 1
                break
            # when user info is correct breaks out of loop and continues to homepage

    elif account_status == 'new account':

        newUCID = input("Enter UCID\n")
        newUsername = input("Enter Username\n")
        newEmail = input("Enter email\n") 
        newType = input("User Type\n")

        SQLDriver.add_new_profile(newUCID, newUsername, newEmail, newType)

    elif account_status == 'delete':
        
        newUCID = input("Enter UCID of account to delete\n")
        SQLDriver.delete_profile(newUCID)
    #user click on certain tab

    input = 'selected tab'

# -----------------------------------------------------------------------------------------------

    if input == 'stats':

        isNewUser = input("Existing user? (Yes or No), to delete stats (Delete)\n")

        if isNewUser == "No":

            stats = SQLDriver.get_user_stats(ucid)

            print("Matches won: " + stats.wins)

            print("Matches played: " + stats.gamesPlayed)

            print("Hours played: " + stats.timeSpent)

        elif isNewUser == "Yes":
            
            newMatchesWon = input("Enter matches won\n")
            newMatchesPlayed = input("Enter matches played\n")
            newHoursPlayed = input("Enter hours played\n")

            SQLDriver.add_stats(ucid, newMatchesWon, newMatchesPlayed, newHoursPlayed )

        elif isNewUser == "Delete":

            dID = input("Enter UCID of account's stats to delete\n")
            SQLDriver.delete_stats(dID)
            
        
# --------------------------------------------------------------------------------------------------------------------------------------------------------

    elif input == 'team':

        status = input("New Team or Delete Existing Team or search stats of all team members\n")

        if status == "new":

            newTeam_ID = input("ID\n")
            newTeam_Name = input("Enter desired team name\n")
            newTeam_Type = input("Enter if the team is singles or doubles\n")

            SQLDriver.new_team(newTeam_ID, newTeam_Name, newTeam_Type)

        elif status == "delete":

            toDel = input("Enter team ID to be deleted\n")

            SQLDriver.delete_team(toDel)

        elif status == "stats":
            
            team_id = input("Enter team ID to see players stats\n")

            team_stats = SQLDriver.get_teamMember_stats(team_id)

            print("Matches won: " + team_stats.wins)

            print("Matches played: " + team_stats.gamesPlayed)

            print("Hours played: " + team_stats.timeSpent)

        user_in_team = input("add new member or remove member or show all teams member is part of\n")

        if user_in_team == "add":

            memID = input("Enter new member id\n")

            SQLDriver.add_team_member(memID)

        elif user_in_team == "remove":

            memID = input("Enter member id\n")

            SQLDriver.remove_team_member(memID)

        elif user_in_team == "stats":

            memID = input("Enter member id\n")

            all_teams = SQLDriver.get_all_teams_with_user(memID)

            print("Player is on team(s): " + all_teams.team + "\n")

# --------------------------------------------------------------------------------------------------------------------------------------------------------

    elif input == "booking":

        booking_status = input("New booking or delete existing?")

        if booking_status == "new":

            selected_table = 2

            



        

