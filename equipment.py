class equipment:

    def __init__(self, eType, eID, eMRT):

        self.type = eType
        self.id = eID
        self.mrt = eMRT

    def get_type(self):

        return self.type

    def set_type(self, newType):

        self.type = newType

    def get_id(self):

        return self.id

    def set_id(self, newID):

        self.type = newID
    
    def get_mrt(self):

        return self.mrt
    
    def set_mrt(self, newMRT):

        self.mrt = newMRT