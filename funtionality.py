import SQLDriver
class start:

    account_status = input("Login or new account or delete account")

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

        newUCID = input("Enter UCID")
        newUsername = input("Enter Username")
        newEmail = input("Enter email") 
        newType = input("User Type")

        SQLDriver.add_new_profile(newUCID, newUsername, newEmail, newType)

    elif account_status == 'delete':
        
        newUCID = input("Enter UCID of account to delete")
        SQLDriver.delete_profile(newUCID)
    #user click on certain tab

    input = 'selected tab'

    if input == 'stats':

        isNewUser = input("Existing user? (Yes or No), to delete stats (Delete) ")

        if isNewUser == "No":

            stats = SQLDriver.get_user_stats(ucid)

            print("Matches won: " + stats.wins)

            print("Matches played: " + stats.gamesPlayed)

            print("Hours played: " + stats.timeSpent)

        elif isNewUser == "Yes":
            
            newMatchesWon = input("Enter matches won")
            newMatchesPlayed = input("Enter matches played")
            newHoursPlayed = input("Enter hours played")

            SQLDriver.add_stats(ucid, newMatchesWon, newMatchesPlayed, newHoursPlayed )

        elif isNewUser == "Delete":

            dID = input("Enter UCID of account's stats to delete")
            SQLDriver.delete_stats(dID)
            
        
# --------------------------------------------------------------------------------------------------------------------------------------------------------

    elif input == 'team':

        status = input("New Team or Delete Existing Team or search stats of all team members")

        if status == "new":

            newTeam_ID = input("ID")
            newTeam_Name = input("Enter desired team name")
            newTeam_Type = input("Enter if the team is singles or doubles")

            SQLDriver.new_team(newTeam_ID, newTeam_Name, newTeam_Type)

        elif status == "delete":

            toDel = input("Enter team ID to be deleted")

            SQLDriver.delete_team(toDel)

        elif status == "stats":
            
            team_id = input("Enter team ID to see players stats")

            team_stats = SQLDriver.get_teamMember_stats(team_id)

            print("Matches won: " + team_stats.wins)

            print("Matches played: " + team_stats.gamesPlayed)

            print("Hours played: " + team_stats.timeSpent)

        user_in_team = input("add new member or remove member or show all teams member is part of")

        if user_in_team == "add":

            memID = input("Enter new member id")

            SQLDriver.add_team_member(memID)

        elif user_in_team == "remove":

            memID = input("Enter member id")

            SQLDriver.remove_team_member(memID)
# --------------------------------------------------------------------------------------------------------------------------------------------------------

    



        

