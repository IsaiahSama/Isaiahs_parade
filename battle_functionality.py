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
    def __init__(self, name="", level=1, tier=1, class_="", health=100, power=10, defense=10, crit_chance=5, ability_1="None", ability_2="None", passive="None", paradians=200, weapon="None", armor="None", player_id=0) -> None:
        self.name = name
        self.level = level 
        self.tier = tier 
        self.class_ = class_ 
        self.health = health
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
    "DEFENSE": 30,
    "CLASS_": "Warrior"
}

ranger_dict = {
    "CRIT_CHANCE":15,
    "CLASS_": "Ranger"
}

mage_dict = {
    "POWER": 25,
    "DEFENSE": -5,
    "CLASS_": "Mage"
}

enemy_dict = {
    "HEALTH": 100,
    "POWER": 15,
    "DEFENSE": 5,
    "EXPGAIN": 20,
    "PARADIANS": 30
}