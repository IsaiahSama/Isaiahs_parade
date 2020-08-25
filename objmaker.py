import discord
from discord.ext import commands, tasks
import asyncio
from cusobj import *
import os
import json

class objcreator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.save.start()

    if not os.path.exists("customobject.json"):
        with open("customobject.json", "w"):
            print("Created file")

    tosave = []

    @commands.command()
    async def createobject(self, ctx):
        await ctx.send("I will ask you some questions about the object you wish to create, and your answers will be used to create it")
        await ctx.send("Type 'ok' if you understand, and anything else if you don't")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await self.bot.wait_for("message", timeout=20, check=check)
        except asyncio.TimeoutError:
            await ctx.channel.send("No response is fine too")
        
        if msg.content.lower() == "ok":
            await ctx.send("Excellent")
            await self.objsel(ctx)
        else:
            await ctx.send("Maybe next time")

    # Functions

    async def objsel(self, ctx):
        await ctx.send("What kind of object would you like to create. Below is a list")
        await ctx.send("Vehicle, furniture, creature.\nSimply type the name of the one you want to create")
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        
        while True:
            try:
                msg = await self.bot.wait_for("message", timeout=20, check=check)
            except asyncio.TimeoutError:
                await ctx.send("Took to long to respond")
                return False

            if msg.content.lower() in ["vehicle", "furniture", "creature"]:
                msg = msg.content.lower()
                await ctx.send(f"Ok, Getting data for making {msg}s ")
                break
            else:
                await ctx.send("That... is not an option. Try again")
                continue

        eval(f"{msg}make(ctx, msg)")

    # Functions

    async def vehiclemake(self, ctx, omaking):
        await ctx.send(f"""Ok. Let us begin creating your {omaking}.
    As I mentioned earlier, I will ask you questions and you will give me responses matching my questions""")

        name = await self.getstrvalue(ctx, "name")
        desc = await self.getstrvalue(ctx, "description")
        color = await self.getstrvalue(ctx, "color")
        numwheels = await self.getnumvalue(ctx, "number of wheels")
        material = await self.getstrvalue(ctx, "material")
        speed = await self.getstrvalue(ctx, "average speed")
        creator = ctx.author.id
        
        product = vehicle(name, desc, color, numwheels, material, speed, creator)
        self.tosave.append(product)

        await ctx.send(f"Congratulations, You have created your {omaking}. View it with <>mycreations")

    async def furnituremake(self, ctx, omaking):
        await ctx.send(f"""Ok. Let us begin creating your {omaking}.
    As I mentioned earlier, I will ask you questions and you will give me responses matching my questions""")

        name = await self.getstrvalue(ctx, "name")
        desc = await self.getstrvalue(ctx, "description")
        color = await self.getstrvalue(ctx, "color")
        numlegs = await self.getnumvalue(ctx, "number of legs")
        material = await self.getstrvalue(ctx, "material")
        creator = ctx.author.id
        
        product = furniture(name, desc, color, numlegs, material, creator)
        self.tosave.append(product)

        await ctx.send(f"Congratulations, You have created your {omaking}. View it with <>mycreations")

    async def creaturemake(self, ctx, omaking):
        await ctx.send(f"""Ok. Let us begin creating your {omaking}.
    As I mentioned earlier, I will ask you questions and you will give me responses matching my questions""")

        name = await self.getstrvalue(ctx, "name")
        desc = await self.getstrvalue(ctx, "description")
        color = await self.getstrvalue(ctx, "color")
        numlegs = await self.getnumvalue(ctx, "number of legs")
        traits = await self.getstrvalue(ctx, "traits")
        typeof = await self.getstrvalue(ctx, "creature type")
        creator = ctx.author.id
        
        product = creature(name, desc, color, numlegs, traits, typeof, creator)
        self.tosave.append(product)

        await ctx.send(f"Congratulations, You have created your {omaking}. View it with <>mycreations")

    # Functions with return values
    async def getstrvalue(self, ctx, valuetoget):
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        while True:
            await ctx.send(f"What is it's {valuetoget}")

            msg = await self.bot.wait_for("message", timeout=20, check=check)

            await ctx.send(f"Ok, so it's {valuetoget} is {msg}? Yes or No")
            newmsg = await self.bot.wait_for("message", timeout=20, check=check)

            if newmsg.content.lower() == "yes":
                await ctx.send("Excellent. Moving on")
                return msg

            elif newmsg.content.lower() == "no":
                await ctx.send("Ok, so we'll go again")
                continue

            else:
                await ctx.send("I didn't understand that response, so we'll go again >:)")
                continue          


    async def getnumvalue(self, ctx, valuetoget):
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        while True:
            await ctx.send(f"What is it's {valuetoget}")

            msg = await self.bot.wait_for("message", timeout=20, check=check)

            try:
                msg = int(msg)
            except ValueError:
                await ctx.send("That is not a number. Try again")
                continue

            await ctx.send(f"Ok, so it's {valuetoget} is {msg}? Yes or No")
            newmsg = await self.bot.wait_for("message", timeout=20, check=check)

            if newmsg.content.lower() == "yes":
                await ctx.send("Excellent. Moving on")
                return msg

            elif newmsg.content.lower() == "no":
                await ctx.send("Ok, so we'll go again")
                continue

            else:
                await ctx.send("I didn't understand that response, so we'll go again >:)")
                continue

    @tasks.loop(minutes=5)
    async def save(self):
        todump = []
        if len(self.tosave) == 0:
            pass
        else:
            for item in self.tosave:
                todump.append(item.__dict__)

            with open("customobject.json", "a") as f:
                json.dump(todump, f, indent=4)

def setup(bot):
    bot.add_cog(objcreator(bot))
