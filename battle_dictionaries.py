# Player Template
player_template = {
    "NAME": "",
    "LIVES": 4,
    "LEVEL": 0,
    "TIER": 1,
    "CLASS": "",
    "HEALTH": 100,
    "POWER": 30,
    "DEFENSE": 10,
    "CRIT_CHANCE": 5,
    "ABILITY_1": "None",
    "ABILITY_2": "None",
    "PARADIANS": 100,
    "WEAPON": "None",
    "ARMOR": "None",
    "EXP": 0,
    "EXP_TO_NEXT_LEVEL": 100,
    "PLAYER_ID": 0
}

# Enemy Template
enemy_template = {
    "NAME": "ENEMY",
    "HEALTH": 100,
    "POWER": 10,
    "DEFENSE": 5, 
    "EXPGAIN": 0,
    "PARADIANS": 0
}

# Battle Dictionaries
class_emojis = {
    "🗡️": "Warrior",
    "🏹": "Ranger",
    "📖": "Mage"
}

all_battle_emojis = {
    "⚔️": "Attack",
    "🥤" : "Potion",
    "⛓" : "Ability_1",
    "👹" : "Ability_2",
    "😇" : "Blessing",
    "🏃" : "Run"
}

# Class Dictionaries
warrior_dict = {
    "POWER": 30,
    "DEFENSE": 30,
    "CLASS": "Warrior"
}

ranger_dict = {
    "CRIT_CHANCE":15,
    "CLASS": "Ranger"
}

mage_dict = {
    "POWER": 40,
    "DEFENSE": -5,
    "CLASS": "Mage"
}

# Ability Dictionaries

abilities = {
    "Warrior": {
        "ABILITY_1": {
            "NAME": "Thrash",
            "TOOLTIP": "A thrashing attack that Triples attack power, but reduces defence by 20%``` https://i.pinimg.com/originals/5b/31/0a/5b310a23d4d2c7879d215eb477590ea6.gif ```diff",
            "CHANCE": 40,
            "PLAYER":{
                "POWER": 300,
                "DEFENSE": -20
            }
        },

        "ABILITY_2": {
            "NAME": "Warrior Cry",
            "TOOLTIP": "A piercing cry which reduces the defense of enemies by 5%, and increases the power of the user by 30, defense by 5%, and health by 10%",
            "CHANCE": 30,
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
            "CHANCE": 40,
            "PLAYER": {
                "POWER": 250
            }
        },

        "ABILITY_2": {
            "NAME": "Sharp Eye",
            "TOOLTIP": "Focusing strength into eyes, critical strike chance is increased by 30%",
            "CHANCE": 30,
            "PLAYER": {
                "CRIT_CHANCE": 30
            }
        }
    },

    "Mage":{
        "ABILITY_1": {
            "NAME": "Great Sage: Explosion!",
            "TOOLTIP": "BAKURETSU!!! A powerful explosion that does 300% damage``` https://i.pinimg.com/originals/c4/07/40/c4074087283441de471b78e0fb56cf25.gif ```diff",
            "CHANCE": 40,
            "PLAYER":{
                "POWER": 300
            }
        },

        "ABILITY_2": {
            "NAME": "Activate Prepared Magic",
            "TOOLTIP": "A pre-prepared spell the reduces all enemy stats by 10%, and increases all user stats by 5%",
            "CHANCE": 30,
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

blessings = {
    "Warrior": {
        "NAME": "Warrior's Blessing",
        "TOOLTIP": "Doubles Current Health, increases attack power by 50%, increases defense by 30%",
        "EFFECTS":{
            "POWER": 50,
            "DEFENSE": 30,
            "HEALTH": 100
        }
    },
    "Ranger": {
        "NAME": "Ranger's Blessing",
        "TOOLTIP": "Increases critical hit chance by 20%, increases damage done by critical hit by 30%",
        "EFFECTS": {
            "CRITICAL_CHANCE": 20,
            "CRITICAL_DAMAGE": 30
        }
    },
    "Mage":{
        "NAME": "Mage's Blessing",
        "TOOLTIP": "Increases power by 50%",
        "EFFECTS":{
            "POWER": 50
        }
    }
}