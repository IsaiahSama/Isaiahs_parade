player_dict = {
    "NAME": "",
    "LEVEL": 1,
    "TIER": 1,
    "CLASS": "",
    "POWER": 10,
    "DEFENSE": 10,
    "CRIT_CHANCE": 5,
    "ABILITY_1": 0,
    "ABILITY_2": 0,
    "PASSIVE": 0,
    "PARADIANS": 200,
    "WEAPON": 0,
    "ARMOR": 0,
    "PLAYER_ID": 0
}

class Player:
    def __init__(self, name="", level=1, tier=1, class_="", power=10, defense=10, crit_chance=5, ability_1=0, ability_2=0, passive=0, paradians=200, weapon=0, armor=0, player_id=0) -> None:
        self.name = name
        self.level = level 
        self.tier = tier 
        self.class_ = class_ 
        self.power = power 
        self.defense = defense 
        self.crit_chance = crit_chance 
        self.ability_1 = ability_1
        self.ability_2 = ability_2
        self.passive = passive
        self.paradians = paradians
        self.weapon = weapon 
        self.armor = armor 
        self.player_id = player_id

warrior_dict = {
    "POWER": 30,
    "DEFENSE": 30
}

ranger_dict = {
    "CRIT_CHANCE":20
}

mage_dict = {
    "POWER": 25,
    "DEFENSE": -5
}

enemy_dict = {
    "HEALTH": 100,
    "POWER": 15,
    "DEFENSE": 5,
    "EXPGAIN": 20,
    "PARADIANS": 30
}