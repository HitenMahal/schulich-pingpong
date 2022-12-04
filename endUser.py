
class endUser:

    def __init__(self, uType, uEmail, uName, uId):

        self.usertype = uType
        self.email = uEmail
        self.name = uName
        self.ucid = uId

    def get_user_Type(self):

        return self.usertype

    def set_user_Type(self, newUser):

        self.usertype = newUser

    def get_email(self):

        return self.user.email

    def set_email(self, newEmail):

        self.email = newEmail
    
    def get_name(self):

        return self.name
    
    def set_name(self, newName):

        self.name = newName

    def get_ucid(self):

        return self.ucid

    def set_ucid(self, newUcid):

        self.ucid = newUcid