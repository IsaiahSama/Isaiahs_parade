# File for Custom Objects.
# All items created will be made using the below classes

class furniture:
    
    def __init__(self, name, description="None", color="Unknown", amountoflegs=0, material="Unknown", creator=None):
        self.name = name
        self.description = description
        self.color = color
        self.amountoflegs = amountoflegs
        self.material = material
        self.creator = creator
        self.objname = "furniture"
       

class creature:
    
    def __init__(self, name, description="None", color="None", amountoflegs=0, traits="None", species="None", creator=None):
        self.name = name
        self.description = description
        self.color = color
        self.species = species
        self.amountoflegs = amountoflegs
        self.traits = traits
        self.creator = creator
        self.objname = "creature"


class vehicle:

    def __init__(self, name, description="None", color="None", numberofwheels=0, material="Unknown", speed=0, creator=None):
        self.name = name
        self.description = description
        self.color = color
        self.numberofwheels = numberofwheels
        self.material = material
        self.speed = speed
        self.creator = creator
        self.objname = "vehicle"

        