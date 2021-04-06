# Dictionaries
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

# Classes
class Player:
    """Class for the player"""
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

class Enemy:
    """Class for the Enemy"""
    def __init__(self, health, power, defense, expgain, paradians) -> None:
        self.health = health 
        self.power = power
        self.defense = defense
        self.expgain = expgain
        self.paradians = paradians

# battle_emojis = {
#         "⚔️": "Attack",
#         "🥤" : "Potion",
#         "⛓" : "Ability_1",
#         "👹" : "Ability_2",
#         "😇" : "Blessing",
#         "🏃" : "Run",
#     }
class BattleHandler:
    """Class that handles the two battle turns"""
    def __init__(self, player, enemy) -> None:
        self.player = player
        self.enemy = enemy

    def handle(self, emoji:str):
        if emoji == "⚔️":
            pass
        elif emoji == "🥤":
            pass
        elif emoji == "⛓":
            pass
        elif emoji == "👹":
            pass
        elif emoji == "😇":
            pass 
        else:
            pass