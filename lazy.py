
with open("fighting.py") as fp:
    x1 = fp.read()

with open("fightdata.json") as fd:
    x2 = fd.read()

while True:
    print("What to find?")
    tochange = input(": ")
    if tochange == "done": break

    print("What to change it to?")
    changed = input(": ")

    x1 = x1.replace(f"abiltag == \"{tochange}\"", f"abiltag == {changed}")
    
    x2 = x2.replace(f"\"{tochange}\"", f"{changed}")


with open("fighting.py", "w") as fp2: 
    fp2.write(x1)

with open("fightdata.json", "w") as fd2:
    fd2.write(x2)