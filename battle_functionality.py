from copy import copy
from random import choice, randint, sample, shuffle

from battle_dictionaries import *

# battle_emojis = {
#         "⚔️": "Attack",
#         "🥤" : "Potion",
#         "⛓" : "Ability_1",
#         "👹" : "Ability_2",
#         "😇" : "Blessing",
#         "🏃" : "Run",
#     }
class BattleHandler:
    """Class that handles all battle related functions"""
    def __init__(self, player, enemy) -> None:
        self.player = player
        self.enemy = enemy

    def handle(self, emoji:str) -> dict:
        """Function that handles the turns for the attacker and defender, returns the message to be output, and the two dictionaries"""
        msg1 = self.handle_user(self.player, self.enemy, emoji)
        msg2 = self.handle_user(self.enemy, self.player, None)
        msg = f"```diff\n+ {msg1}\n- {msg2}```"
        return msg, self.player, self.enemy

    def handle_user(self, attacker, defender, emoji) -> str:
        """Determines the action to take based on the used emoji. Currently for enemies, all they can do is attack. Returns the message to be output"""
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
            msg = self.handle_blessing(attacker)
        else:
            can_run = self.handle_running(attacker, defender)
            if can_run:
                if attacker["PARADIANS"] == 0:
                    attacker['PARADIANS'] -= 100
                    msg = f"RUN SUCCESSFUL: {attacker['NAME']} was saved by wandering traveler, but is too poor to pay them, so now they owe Lady Luck {attacker['PARADIANS']} paradians"
                else:
                    attacker["PARADIANS"] -= (1/5) * attacker["PARADIANS"]
                    msg = f"RUN SUCCESSFUL: {attacker['NAME']} has escaped from enemy but lost 1/5 of their Paradians in the process"
            else:
                msg = f"RUN FAILED: {attacker['NAME']} has failed to escape from enemy"

        return msg        

    def handle_attack(self, attacker, defender) -> str:
        """Handles the attacking and life deduction. Returns the message to be output"""
        power = self.get_power(attacker)
        is_crit = False
        if hasattr(attacker, "crit_chance"):
            power, is_crit = self.handle_crit(power, attacker, is_crit)
        
        power -= (defender["DEFENSE"] // 2)
        if power < 0: power = 1
        defender["HEALTH"] -= power

        if is_crit:
            return f"IT'S A CRIT. {attacker['NAME']} attacked {defender['NAME']} and did a whoppin {power} damage"
        else:
            return f"{defender['NAME']} was attacked by {attacker['NAME']} and took {power} damage"


    def handle_potion(self, attacker) -> str:
        """Determines if a player can heal or not. If so, performs the heal, and then returns the message to be output"""
        options = [True, True, True, False, False]
        shuffle(options)
        will_heal = choice(options)
        if not will_heal:
            return f"{attacker['NAME']} tried to heal but was in a hurry and spilt the potion"

        heal_amount = randint((attacker["HEALTH"]//10), (attacker["HEALTH"]//5))
        attacker["HEALTH"] += heal_amount
        return f"{attacker['NAME']} healed for {heal_amount} health"


    def handle_ability_1(self, attacker, defender) -> str:
        """Function which passes on the values to the ability handler, then returns the message"""
        ability = abilities[attacker["CLASS"]]["ABILITY_1"]
        msg = self.handle_ability(attacker, defender, ability)
        return msg

    def handle_ability_2(self, attacker, defender) -> str:
        """Function which passes on the values to the ability handler, then returns the message"""
        ability = abilities[attacker["CLASS"]]["ABILITY_2"]
        msg = self.handle_ability(attacker, defender, ability)
        return msg        

    def handle_blessing(self, attacker) -> str:
        """Uses the blessing of the attacker. Returns the message to be output"""
        blessing = blessings[attacker["CLASS"]]
        for k, v in blessing['EFFECTS'].items():
            value = attacker.get(k, None)
            if not value:
                attacker[k] = v
            else:
                print(attacker[k])
                attacker[k] += round(v/100 * value)
                print(attacker[k])

        msg = f"I, {attacker['NAME']}, have been blessed. {blessing['NAME']}: {blessing['TOOLTIP']}"
        return msg

    def handle_running(self, attacker, defender) -> bool:
        """Determines whether or not the player is able to run. Returns this as a boolean"""
        health_difference = abs(defender['HEALTH'] - attacker['HEALTH']) + 100
        return self.random_calculator(list(range(0, 100)), health_difference % 100)
        
    def get_power(self, attacker) -> int:
        """Calculates the varying power of the attacker. Returns the power as an integer"""
        return randint(attacker["POWER"]-5, attacker["POWER"]+6)

    def handle_ability(self, attacker, defender, ability) -> str:
        """Determines if an ability can is used or not. If so, applies the affect of the ability. Returns a string containing the message to output"""
        msg = f"Ability Activate: {ability['NAME']}: {ability['TOOLTIP']}"
        can_ability = self.random_calculator(range(0, 100), ability["CHANCE"])
        if not can_ability:
            msg += f"\nAbility failed"
            return msg
        power = self.get_power(attacker)
        for k, v in ability["PLAYER"].items():
            if k == "POWER":
                power += v/100 * attacker["POWER"]
                continue
            attacker[k] = round((v/100 * attacker[k]) + attacker[k])

        enemy_effects = ability.get("ENEMY", None)
        if enemy_effects:
            for k, v in ability["ENEMY"].items():
                defender[k] += v

        if ability["PLAYER"].get("POWER", None):
            defender["HEALTH"] -= power 
            msg += f"\n+ {defender['NAME']} took {power} damage from {attacker['NAME']}'s {ability['NAME']}"

        return msg

    def handle_crit(self, power, attacker, is_crit) -> bool:
        """Calculates whether of not a crit will occur, and determines the output. Returns the power as a float and the crit as a bool"""
        
        crit_chance = attacker.crit_chance
        
        if attacker.get("CRITICAL_CHANCE", None):
            crit_chance += attacker["CRITICAL_CHANCE"]

        is_crit = self.random_calculator(range(0, 100), attacker.crit_chance)
        if is_crit:
            power *= 1.5

        if attacker.get("CRITICAL_DAMAGE", None):
            power += round((attacker["CRITICAL_DAMAGE"] / 100) * power)

        return power, is_crit

    def random_calculator(self, numrange:list, percent_value:int) -> bool:
        """Calculates whether a certain event will occur or not. Takes a range of numbers, and a percent value as an integer. Returns the boolean."""
        numbers = sample(numrange, round((percent_value/100) * (len(numrange) - 1)))
        value = randint(numrange[0], numrange[-1])

        if value in numbers:
            return True 
        return False

    def get_battle_emojis(self, player) -> dict:
        """Used to determine what emojis will be available for the user to use. Returns a dictionary of emojis to action"""
        # battle_emojis = {"⚔️": "Attack", "🥤" : "Potion", "🏃" : "Run"}
        # if player["LEVEL"] >= 20:
        #     battle_emojis["⛓"] = "Ability_1"
        # if player["LEVEL"] >= 40:
        #     battle_emojis["👹"] = "Ability_2"
        # if player["LEVEL"] >= 60:
        #     battle_emojis["😇"] = "Blessing"

        return all_battle_emojis

    def handle_level_up(self, player):
        msg = ""
        player["LEVEL"] += 1
        msg += f"!!!\n{player['NAME']} is now level {player['LEVEL']}"

        if player["LEVEL"] % 100 == 0 and player["LEVEL"] < 5:
            player["TIER"] += 1
            msg += f"\n!!! {player['NAME']} is now Tier {player['TIER']}"

        player["EXP_FOR_NEXT_LEVEL"] *= 1.6

        return msg, player

def handle_enemy_gen(player):
    # Function which handles the generation of enemies.

    def variate(value) -> int:
        # Function which takes in a value, and returns a variaton of that number
        number = randint(1, (value // 2))

        if number % 2 == 0:
            return value + number
        else:
            return value - number

    enemy = copy(enemy_template)

    enemy["HEALTH"] = variate(player["MAX_HEALTH"])
    enemy["POWER"] = variate(player["POWER"])
    enemy["DEFENSE"] = variate(player["DEFENSE"])

    enemy["EXPGAIN"] = round((1 / variate(10)) * player["EXP_FOR_NEXT_LEVEL"])

    enemy["PARADIANS"] = round((1 / randint(2, 5)) * ((player["MAX_HEALTH"] + player["POWER"]) // 5))

    print(enemy)

    return enemy
