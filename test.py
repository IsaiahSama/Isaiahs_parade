# Here we will read through some quick values and print out the exp ranges at each level
import random
from fight import BeastFight, enemybeta
base = 50
current = 0
level = 0
maxlevel = 50

with open("temp.txt", "w"):
    print("Created File")

while level < 301:
    for level in range(maxlevel):
        base += 30
        level += 1
    
    maxlevel += 50
    lowest = round((1/25) * base)
    highest = round((1/6) * base)
    lvlrange = [random.randint(lowest, highest) for x in range(8)]
    print(lvlrange)
    with open("temp.txt", "a") as f:
        f.write(f"At level {level} you will need {base} exp to level up\n")
        f.write(f"Weakest will have {lowest} exp\n\n")
        for enemy in sorted(lvlrange):
            f.write(f"Exp will be {enemy}\n")
        f.write(f"Strongest will have {highest} exp\n\n")

tier1 = [x.mindmg for x in enemybeta if x.level in range(0, 50)]
tier2 = [x.mindmg for x in enemybeta if x.level in range(50, 100)]
tier3 = [x.mindmg for x in enemybeta if x.level in range(100, 150)]
tier4 = [x.mindmg for x in enemybeta if x.level in range(150, 200)]
tier5 = [x.mindmg for x in enemybeta if x.level in range(200, 500)]


print(f"Highest: {max(tier1)}")
print(f"Highest: {max(tier2)}")
print(f"Highest: {max(tier3)}")
print(f"Highest: {max(tier4)}")
print(f"Highest: {max(tier5)}")

