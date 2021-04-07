from random import choice, randint, sample, shuffle
# Class Dictionaries
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

# Ability Dictionaries

abilities = {
    "Warrior": {
        "ABILITY_1": {
            "NAME": "Thrash",
            "TOOLTIP": "A thrashing attack that Triples attack power, but reduces defence by 20%``` https://i.pinimg.com/originals/5b/31/0a/5b310a23d4d2c7879d215eb477590ea6.gif ```diff",
            "PLAYER":{
                "POWER": 300,
                "DEFENSE": -20
            }
        },

        "ABILITY_2": {
            "NAME": "Warrior Cry",
            "TOOLTIP": "A piercing cry which reduces the defense of enemies by 5%, and increases the power of the user by 30, defense by 5%, and health by 10%",
            "PLAYER": {
                "POWER": 30,
                "DEFENSE": 5,
                "HEALTH": 10
            },
            "ENEMY":{
                "DEFENSE": -5
            }
        }
    },

    "Ranger": {
        "ABILITY_1": {
            "NAME": "Ballista Shot",
            "TOOLTIP": "Fires a powerful piercing shot which does 250% of power``` https://static.wikia.nocookie.net/terraria_gamepedia/images/e/ee/Ballista_Cane_%28demo%29.gif ```diff",
            "PLAYER": {
                "POWER": 250
            }
        },

        "ABILITY_2": {
            "NAME": "Sharp Eye",
            "TOOLTIP": "Focusing strength into eyes, critical strike chance is increased by 30%",
            "PLAYER": {
                "CRIT_CHANCE": 30
            }
        }
    },

    "Mage":{
        "ABILITY_1": {
            "NAME": "Great Sage: Explosion!",
            "TOOLTIP": "BAKURETSU!!! A powerful explosion that does 300% damage``` https://i.pinimg.com/originals/c4/07/40/c4074087283441de471b78e0fb56cf25.gif ```diff",
            "PLAYER":{
                "POWER": 300
            }
        },

        "ABILITY_2": {
            "NAME": "Activate Prepared Magic",
            "TOOLTIP": "A pre-prepared spell the reduces all enemy stats by 10%, and increases all user stats by 5%",
            "ENEMY":{
                "DEFENSE": -10,
                "POWER": -10,
                "HEALTH": -10
            },
            "PLAYER":{
                "HEALTH": 5,
                "DEFENSE": 5,
                "CRIT_CHANCE": 5
            }
        }
    }
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
            msg = self.handle_ability_1(attacker, defender)
        elif emoji == "👹":
            msg = self.handle_ability_2(attacker, defender)
        elif emoji == "😇":
            msg = "This Feature is not available as yet."
        else:
            pass

        return msg        

    def handle_attack(self, attacker, defender):
        power = self.get_power(attacker)
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


    def handle_ability_1(self, attacker, defender):
        ability = abilities[attacker.class_]["ABILITY_1"]
        msg = self.handle_ability(attacker, defender, ability)
        return msg

    def handle_ability_2(self, attacker, defender):
        ability = abilities[attacker.class_]["ABILITY_2"]
        msg = self.handle_ability(attacker, defender, ability)
        return msg        

    def handle_blessing(self):
        pass 

    def handle_running(self):
        pass

    def get_power(self, attacker):
        return randint(attacker.power-5, attacker.power+6)

    def handle_ability(self, attacker, defender, ability):
        msg = f"Ability Activate: {ability['NAME']}: {ability['TOOLTIP']}"
        power = self.get_power(attacker)
        for k, v in ability["PLAYER"].items():
            if k == "POWER":
                power += v/100 * getattr(attacker, "power")
                continue
            setattr(attacker, k.lower(), getattr(attacker, k.lower()) + ((v//100) * getattr(attacker, k.lower())))

        enemy_effects = ability.get("ENEMY", None)
        if enemy_effects:
            for k, v in ability["ENEMY"].items():
                setattr(defender, k.lower(), getattr(defender, k.lower()) + v)

        if ability["PLAYER"].get("POWER", None):
            defender.health -= power 
            msg += f"\n+ {defender.name} took {power} damage from {attacker.name}'s {ability['NAME']}"

        return msg

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
