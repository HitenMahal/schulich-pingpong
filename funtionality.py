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

    elif delete_profile == 'delete':
        
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

        team = SQLDriver.teamInfo(ucid)# player ucid will be sent in to then pull info about the team they are in
        
        print("Team name: " + team.teamName)

        #Realized a player could be part of more than 1 team, could make life easier and only show 1 player can only be on 1 team
        #If want to show player with multiple teams ->
        # Need to make loop to check for all teams players is part of
        # then  print out every information about that specific team

        print("Team Type: " + team.teamType)

        print("Team ID: " + team.id)

        print("Team Members: " + team.member1 + team.member2)

        #attempt to print off all teams user is in

        numOfTeam = SQLDriver.teamInfo(ucid)     # count through the number of teams the player is part of

        for i in numOfTeam:
            
            #will iterate throught he teams the player is in

            if team.type == 'singles':

                print("Team name: " + team.teamName)

                print("Team Type: " + team.teamType)

                print("Team ID: " + team.id)

                print("Team Members: " + ucid)

            elif team.type == 'doubles':

                print("Team name: " + team.teamName)

                print("Team Type: " + team.teamType)

                print("Team ID: " + team.id)

                print("Team Members: " + ucid + team.partnerID)

            # move onto next team\

        
# --------------------------------------------------------------------------------------------------------------------------------------------------------

    elif input == 'booking':

        checker = 0

        while checker == 0:

            building_input = input("Select Building")

            building_name = SQLDriver.Building(building_input) #see if requested building is valid

            if building_name == 1:

                table_input = input("Select a table to play at")

                table_id = SQLDriver.table(table_input, building_name.name) # check if table exists

                if table_id == 1:

                    requested_time = input("Select a time slot")

                    schedule_id = SQLDriver.schedule(table_id.id, building_name.name, requested_time)

                    if schedule_id == 1:

                        print("Time slot resevered for " + username + " in " + building_name.name + " ,table " + table_id.id + " at " + schedule_id.time)

                        checker = 1
                        
                        
                    else:

                        print("Time slot not available")

                else:

                    print("Table not valid")

            else:

                print("Building not valid")        







        

