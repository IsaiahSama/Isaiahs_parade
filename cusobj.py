# File for Custom Objects.
# All items created will be made using the below classes

class furniture:
    
    def __init__(self, name, description="None", color="Unknown", amountoflegs=0, material="Unknown", creator=None):
        self.name = name
        self.description = description
        self.color = color
        self.material = material
        self.amountoflegs = amountoflegs
        self.creator = creator

class creature:
    
    def __init__(self, name, description="None", color="None", amountoflegs=0, traits="None", typeof="None", creator=None):
        self.name = name
        self.description = description
        self.amountoflegs = amountoflegs
        self.traits = traits
        self.color = color
        self.typepf = typeof
        self.creator = creator

class vehicle:

    def __init__(self, name, description="None", color="None", numberofwheels=0, material="Unknown", speed=0, creator=None):
        self.name = name
        self.description = description
        self.color = color
        self.numberofwheels = numberofwheels
        self.material = material
        self.speed = speed
        self.creator = creator