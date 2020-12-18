import asyncio
import json
from teams import Team
from fight import Fighter
from relastatus import Relauser
import os

class Saving:
    "Class Used for saving json files"
    
    def __init__(self):
        pass
    
    async def loaddata(self, folder):
        files = os.listdir(f"saves/{folder}")
        print(f"Attempting to load data from {folder}")
        if not files: print("No previous saves exist"); return
        data = await self.getdata(folder, files)
        if not data: return []
        datalist = []
        for dic in data:
            if folder == "fightdata":
                u = Fighter(dic["name"], dic["tag"], dic["level"], dic['curxp'], dic['health'], dic['mindmg'], dic['maxdmg'], dic['wins'], dic['losses'], dic['pcoin'])
            elif folder == "teamdata":
                u = Team()
            else:
                u = Relauser(dic['guild'], dic['name'], dic['tag'])
            
            for k, v in dic.items():
                setattr(u, k, v)
                datalist.append(u)

        return datalist

    async def getdata(self, folder, files):
        index = -1
        while True:
            try:
                with open(f"saves/{folder}/{files[index]}") as f:
                    data = json.load(f)
                    print(f"Loaded data from {files[index]}")
                    return data
            except json.JSONDecodeError:
                print(f"{files[index]} was responsible for the JSONDecodeError")
                os.remove(f"saves/{folder}/{files[index]}")
                index -= 1
            except IndexError:
                print(f"There aren't any {folder} files for me to read :(")
                return []
            
    async def save(self, folder, data):
        files = os.listdir(f"saves/{folder}")
        dumped = [member.__dict__ for member in data]
        if not files:
            with open(f"saves/{folder}/{folder}0.json") as f:
                json.dump(dumped, f, indent=4)
                return

        if len(files) == 10: await self.savefix(folder, files)
        with open(f"saves/{folder}/{folder}{int(list(files[-1].split('.')[0])[-1]) + 1}.json", "w") as f:
            json.dump(dumped, f, indent=4)

    async def savefix(self, folder, files):
        os.remove(f"saves/{folder}/{files[0]}")
        files.remove(files[0])
        for pos, file in enumerate(files):
            os.rename(f"saves/{folder}/{file}", f"saves/{folder}/{''.join(list(file.split('.')[0]).pop())}{pos}.json")
  