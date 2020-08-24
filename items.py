from dataclasses import dataclass, field

@dataclass()
class Item:
    name: str
    tag: int
    desc: str
    cost: int
    effect: str
    duration: int
    tierz: int
    hup: int
    pup: int
    minup: int
    maxup: int
    critup: int
    untype: str 
    typeobj: str="item"
    

# Buff Potions
# name, tag, desc, cost, effect, duration, tier, healthup, powerup, minup, maxup, critup, untype(pot or item)
ppot = Item("Power Potion", 100, "A basic potion which increases your attack power by 20 for 3 fights",
500, "increases attack power by 20", 3, 1, 0, 20, 0, 0, 0, "pot")
hpot = Item("Health Potion", 101, "A basic health potion which increases your health by 30 for 2 fights",
600, "Increases health by 30", 2, 1, 30, 0, 0, 0, 0, "pot")
lblet = Item("Lucky Bracelet", 102, "A bracelet which increases your crit chance by 10% for 2 fights",
650, "Increases Crit Chance by 10%", 2, 1, 0, 0, 0, 0, 10, "item")
mpot = Item("Mixa Pot", 104, "A potion carefully brewed increasing your power and health by 50 for 2 fights",
1100, "Increases health and power by 50", 2, 2, 50, 50, 0, 0, 0, "pot")
sring = Item("Special Ring", 105, "A ring which increases your min and max damage by 30 for 3 fights",
1200, "Increases min and max damage by 30", 3, 2, 0, 0, 30, 30, 0, "item")
mcloak = Item("Magic Cloak", 106, "Fairly dusty, but seems to increase all of your stats by 15 for 5 fights",
1000, "Increases all stats by 15", 5, 2, 15, 15, 15, 15, 15, "item")
gpapple = Item("Golden Pineapple", 107, "A golden pineapple that when it's juice is drunk, increases health by 150 and power by 40 for 2 fights",
2300, "Increases health by 150, and power by 40", 2, 3, 150, 40, 0, 0, 0, "pot")

potlist = [ppot, hpot, lblet, mpot, sring, mcloak, gpapple]

