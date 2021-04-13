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

    def handle_attack(self, attacker, defender):
        power = self.get_power(attacker)
        is_crit = False
        if hasattr(attacker, "crit_chance"):
            power, is_crit = self.handle_crit(power, attacker, is_crit)
        
        power -= (defender.defense // 2)
        if power < 0: power = 1
        defender["HEALTH"] -= power

        if is_crit:
            return f"IT'S A CRIT. {attacker['NAME']} attacked {defender['NAME']} and did a whoppin {power} damage"
        else:
            return f"{defender['NAME']} was attacked by {attacker['NAME']} and took {power} damage"


    def handle_potion(self, attacker):
        options = [True, True, True, False, False]
        shuffle(options)
        will_heal = choice(options)
        if not will_heal:
            return f"{attacker['NAME']} tried to heal but was in a hurry and spilt the potion"

        heal_amount = randint((attacker["HEALTH"]//10), (attacker["HEALTH"]//5))
        attacker["HEALTH"] += heal_amount
        return f"{attacker['NAME']} healed for {heal_amount} health"


    def handle_ability_1(self, attacker, defender):
        ability = abilities[attacker["CLASS"]]["ABILITY_1"]
        msg = self.handle_ability(attacker, defender, ability)
        return msg

    def handle_ability_2(self, attacker, defender):
        ability = abilities[attacker["CLASS"]]["ABILITY_2"]
        msg = self.handle_ability(attacker, defender, ability)
        return msg        

    def handle_blessing(self, attacker):
        blessing = blessings[attacker["CLASS"]]
        for k, v in blessing.items():
            value = attacker.get(k)
            if not value:
                attacker[k] = v
            else:
                attacker[k] = (v/100 * value) + value

        msg = f"I, {attacker['name']}, have been blessed. {blessing['NAME']}: {blessing['TOOLTIP']}"
        return msg

    def handle_running(self, attacker, defender):
        health_difference = abs(defender['health'] - attacker['health']) + 100
        return self.random_calculator(list(range(0, 100)), health_difference % 100)
        
    def get_power(self, attacker):
        return randint(attacker["POWER"]-5, attacker["POWER"]+6)

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
            defender["HEALTH"] -= power 
            msg += f"\n+ {defender['NAME']} took {power} damage from {attacker['NAME']}'s {ability['NAME']}"

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
