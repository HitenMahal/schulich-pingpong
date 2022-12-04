class building:

    def __init__(self, bName, bLocation, bFac):

        self.name = bName
        self.location = bLocation
        self.fac = bFac

    def get_building_name(self):

        return self.name

    def set_building_name(self, newName):

        self.name = newName

    def get_location(self):

        return self.location
    
    def set_location(self, newLocation):

        self.location = newLocation

    def get_fac(self):

        return self.fac

    def set_fac(self, newFac):

        self.fac = newFac

