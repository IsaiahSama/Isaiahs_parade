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
    typeobj: str
    

# Buff Potions
# name, tag, desc, cost, effect, duration, tier, hup, pup, minup, maxup, critup, typez
ppot = Item("Power Potion", 100, "A basic potion which increases your attack power by 20 for 3 minutes",
500, "increases attack power by 20", 3, 1, 0, 20, 0, 0, 0, "pot", "item")

potlist = [ppot]

