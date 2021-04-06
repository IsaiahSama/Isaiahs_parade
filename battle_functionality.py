from random import choice, randint, sample, shuffle
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
    def __init__(self, name="Enemy", health=100, power=15, defense=10, expgain=100, paradians=100) -> None:
        self.name = name
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
        msg1 = self.handle_user(self.player, self.enemy, emoji)
        msg2 = self.handle_user(self.enemy, self.player, None)
        msg = f"```diff\n+ {msg1}\n- {msg2}```"
        return msg, self.player, self.enemy

    def handle_user(self, attacker, defender, emoji):
        if not emoji:
            emoji = choice(["⚔️"])

        if emoji == "⚔️":
            msg = self.handle_attack(attacker, defender)
        elif emoji == "🥤":
            msg = self.handle_potion(attacker)
        elif emoji == "⛓":
            pass
        elif emoji == "👹":
            pass
        elif emoji == "😇":
            pass 
        else:
            pass

        return msg        

    def handle_attack(self, attacker, defender):
        power = randint(attacker.power-5, attacker.power+6)
        is_crit = False
        if hasattr(attacker, "crit_chance"):
            power, is_crit = self.handle_crit(power, attacker, is_crit)
        
        power -= (defender.defense // 2)
        if power < 0: power = 1
        defender.health -= power

        if is_crit:
            return f"IT'S A CRIT. {attacker.name} attacked {defender.name} and did a whoppin {power} damage"
        else:
            return f"{defender.name} was attacked by {attacker.name} and took {power} damage"


    def handle_potion(self, attacker):
        options = [True, True, True, False, False]
        shuffle(options)
        will_heal = choice(options)
        if not will_heal:
            return f"{attacker.name} tried to heal but was in a hurry and spilt the potion"

        heal_amount = randint((attacker.health//10), (attacker.health//5))
        attacker.health += heal_amount
        return f"{attacker.name} healed for {heal_amount} health"


    def handle_ability_1(self):
        pass 

    def handle_ability_2(self):
        pass

    def handle_blessing(self):
        pass 

    def handle_running(self):
        pass

    def handle_crit(self, power, attacker, is_crit):
        is_crit = self.random_calculator(range(0, 100), attacker.crit_chance)
        if is_crit:
            power *= 1.5

        return power, is_crit

    def random_calculator(self, numrange:list, percent_value:int):
        numbers = sample(numrange, percent_value)
        value = randint(numrange[0], numrange[-1])

        if value in numbers:
            return True 
        return False
