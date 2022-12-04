class start:

    validUser = 0 # starts with user info is incorrect

    while validUser == 0:

        username = input("Enter Username: ")

        password = input("Enter Password: ")

        ucid = input("Enter UCID: ")

        SQLDriver.loginUser(username, password, ucid) #login start
        # Returns true (1) if user info is correct, returns false (0) if info is incorrect

        if 1:

            validUser = 1
            break
        # when user info is correct breaks out of loop and continues to homepage



    #user click on certain tab

    input = 'selected tab'

    if input == 'stats':

        stats = SQLDriver.userStats(ucid)

        print("Matches won: " + stats.wins)

        print("Matches played: " + stats.gamesPlayed)

        print("Hours played: " + stats.timeSpent)

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

        





        

