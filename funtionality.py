class start:

    validUser = 0 # starts with user info is incorrect

    while validUser == 0:

        username = input("Enter Username: ")

        password = input("Enter Password: ")

        SQLDriver.loginUser(username, password) #login start
        # Returns true (1) if user info is correct, returns false (0) if info is incorrect

        if 1:

            validUser = 1
            break
        # when user info is correct breaks out of loop and continues to homepage
        
    #user click on certain tab

    input = 'selected tab'

    if input == 'stats':

        SQLDriver.