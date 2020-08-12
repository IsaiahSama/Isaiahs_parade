import discord
from discord.ext import commands
import asyncio
import random
from random import randint
from isaiahball import responses


class Miscgen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    # Secret messages
    @commands.command()
    async def hme(self, ctx, *, arg):
        msgembed = discord.Embed(
            title="Hidden user said:",
            description=f"{arg}",
            color=randint(0, 0xffffff)
        )

        await ctx.send(embed=msgembed)
        await ctx.message.delete()

    # Fake deathnote
    @commands.command()
    async def fdeathnote(self, ctx, member: discord.Member):
        await ctx.send("***Now that I have my potato chips... you only have 60 seconds to live...***")
        await ctx.send(file=discord.File("images/pchip.gif"))
        await asyncio.sleep(30)
        await ctx.send(f"***30 seconds remain {member.display_name}***")
        await asyncio.sleep(25)
        await ctx.send(f"***It is done... goodbye {member.display_name}. You were pathetic compared to L***")
        await asyncio.sleep(15)
        await ctx.send(f"*I was only kidding you are good {member.display_name}*")



class CallMisc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    channel1 = None
    channel2 = None
    callpending = False
    incall = False
    guild1 = None
    guild2 = None

    """msgembed1 = discord.Embed(
        title=f"{message.author.display_name}",
        description=f"{message}",
        color=rolecolor
    )"""
    
    @commands.command()
    async def intercom(self, ctx):
        if not self.callpending and not self.incall:
            self.guild1 = ctx.guild
            self.channel1 = ctx.channel
            choosing = True
            while choosing:
                self.guild2 = random.choice(self.bot.guilds)
                if self.guild2 == ctx.guild:
                    continue
                else:
                    choosing = False
                if self.guild2.id == 739229902921793637:
                    self.channel2 = self.guild2.get_channel(739236024898682939)
                else:
                    self.channel2 = discord.utils.get(self.guild2.text_channels, name="parade-room")
                    if self.channel2 == None:
                        await self.guild2.create_text_channel("parade-room")
                        for tchan in self.guild2.text_channels:
                            if tchan.name.lower() == "parade-room":
                                await tchan.send("Successfully Created")

                        self.channel2 = discord.utils.get(self.guild2.text_channels, name="parade-room")  
                
            await ctx.send(f"Your intercom request has been sent to {self.guild2.name}")
            await self.channel2.send(f"{ctx.guild.name}, has sent you an intercome request. Accept with <>accept")
            self.callpending = True

            await asyncio.sleep(90)
            if self.callpending:
                await ctx.send(f"It would appear that no one from {self.guild2} has answered your call. Try again later? :shrug:")
                self.callpending = False
        
        elif self.callpending:
            await ctx.send("A call is already pending. You can accept with <>accept")

        elif self.incall:
            await ctx.send("A call is already in progress. Sorry for the inconvenience")

        else:
            pass

    @commands.command()
    async def accept(self, ctx):
        if ctx.channel == self.channel1:
            pass
        elif self.callpending and ctx.channel == self.channel2:
            await ctx.send("Connected")
            await self.channel1.send("Connected")
            self.callpending = False
            self.incall = True

        elif self.callpending and ctx.channel is not self.channel2:
            await ctx.send("Call intercepted.")
            await self.channel1.send(f"Your call has been intercepted by {ctx.guild}")
            await self.channel2.send("The intercom has been intercepted, therefore you can no longer join")
            await ctx.send(f"Connected with {self.guild1.name}")
            self.channel2 = ctx.channel
            self.guild2 = ctx.guild
            self.callpending = False
            self.incall = True

        elif not self.callpending:
            await ctx.send("There is no call currently pending")

    @commands.command()
    async def emoji(self, ctx, arg):
        await ctx.message.delete()
        await ctx.send(f"{ctx.author.display_name}: :{arg}:")
    
    @commands.command()
    async def deny(self, ctx):
        if self.callpending:
            if ctx.channel == self.channel1:
                await ctx.send("You have canceled your request")
                await self.channel2.send("The Request has been canceled")
                self.callpending = False

            elif ctx.channel == self.channel2:
                await ctx.send("You have denied the intercom")
                await self.channel1.send(f"{ctx.guild} has denied your request to intercom")
                self.callpending = False
                
        else:
            await ctx.send("There is no currently pending call")

    @commands.command()
    async def endcall(self, ctx):
        if self.incall:
            if ctx.channel == self.channel1 or ctx.channel == self.channel2:
                self.incall = False
                await self.channel1.send("Ended Call")
                await self.channel2.send("Ended Call")
                self.clear()

    @commands.command()
    async def ping(self, ctx):
        x = round(self.bot.latency * 1000)
        if x <= 100:
            await ctx.send(f"{x}ms. Excellent I daresay")
        elif x >= 101 and x <= 300:
            await ctx.send(f"{x}ms. Not my best but Let's goooo")
        else:
            await ctx.send(f"{x}ms. I don't feel to good, sorry for any delay")


    isaiah = 493839592835907594
    def revealcategory(self):
        return random.choice(responses)

    def revealanswer(self,x):
        return random.choice(x)

    
    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author == self.bot.user:
            return

        msgembed1 = discord.Embed(
            title=f"{message.author.display_name}",
            description=f"{message.content}",
            color=randint(0, 0xffffff)
        )
        
        if self.incall:
            if message.channel == self.channel1 or message.channel == self.channel2:
                await message.delete()
                await self.channel1.send(embed=msgembed1)
                await self.channel2.send(embed=msgembed1)

        if message.content.lower().startswith("oh truth seeking orbs") and message.content.lower().endswith("?"):
            if "isaiah" in message.content.lower():
                await message.channel.send("I'm not answering anything regarding my namesake")
                return
            else:
                await message.channel.send(file=discord.File("images/tso.gif"))
                await message.channel.send("The truth seeking orbs shall analyze your question")
                category = self.revealcategory()
                answer = self.revealanswer(category)
                await asyncio.sleep(5)
                truth = discord.Embed(
                    title="Our Decision",
                    description=f"Our response to your question has been decided {message.author.mention}.",
                    color=randint(0, 0xffffff)
                )

                truth.add_field(name="Response", value=f"{answer}")

                await message.channel.send(embed=truth)
            
        elif message.content.lower().startswith("oh truth seeking orbs") and not message.content.endswith("?"):
            await message.channel.send("If you were trying to get the advice of the Truth seeking Orbs, remember to end your question with a question mark.")

        # Looks for THE WORLD
        if "the world" in message.content.lower():
            if message.author.id == self.isaiah:
                await message.channel.send("Did you mean... ZA WARUDO!?")

        # Thanks
        if message.content.lower == "thanks" or message.content.lower() == "thx":
            if message.author.id == self.isaiah:
                await message.channel.send(f"No problem. Glad to be of assistance to you {message.author.mention}")        


    def clear(self):
        self.channel1 = None
        self.channel2 = None
        self.callpending = False
        self.incall = False
        self.guild1 = None
        self.guild2 = None

class getmentioned(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mentioned(self, ctx):
        msgcount = 0
        for m in await ctx.channel.history().flatten():
            if msgcount < 700:
                if ctx.author in m.mentions:
                    if m.author == self.bot.user:
                        continue
                    await ctx.send(f"{m.author}: ***{m.content}***")
                    return True
                msgcount += 1

        await ctx.send("You weren't recently mentioned")




class GCallMisc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    calledServers = []
    calledChannels = []
    incall = False
    pending = False

    @commands.command()
    async def gcall(self, ctx):
        if not self.incall and not self.pending:
            for server in self.bot.guilds:
                if server == ctx.guild:
                    continue
                else:
                    if server.id == 739229902921793637:
                        channel = server.get_channel(739235964542648411)
                    else:
                        channel = discord.utils.get(server.text_channels, name="parade-room")
                        if channel == None:
                            await server.create_text_channel("parade-room")
                            for tchan in server.text_channels:
                                if tchan.name.lower() == "parade-room":
                                    await tchan.send("Successfully Created")

                            channel = discord.utils.get(server.text_channels, name="parade-room")

                await channel.send(f"Server: {ctx.guild} has started a Multi-Server Intercom. Join with <>gjoin")

            await ctx.send("Your request has been echoed throughout the lands")
            self.pending = True
            self.calledServers.append(ctx.guild.name)
            self.calledChannels.append(ctx.channel)

            await asyncio.sleep(90)
            if self.pending:
                await ctx.send("How unfortunate, It would appear as though no one answered, maybe later?")
                self.pending = False
                self.calledServers.clear()
                return

        elif self.incall:
            await ctx.send("There is already a Multi-Server intercom. Join with <>gjoin")

        elif self.pending:
            await ctx.send("A Multi-Server Intercom is already Pending. Join with <>gjoin")

        else:
            await ctx.send("Unknown Error Occured")

    
    @commands.command()
    async def gjoin(self, ctx):
        if self.pending or self.incall:
            if ctx.channel in self.calledChannels:
                await ctx.send("You are already in the Multi-Server Call")
            
            else:
                self.calledServers.append(ctx.guild.name)
                self.calledChannels.append(ctx.channel)
                for tchan in self.calledChannels:
                    await tchan.send(f"{ctx.guild} has joined the Multi Server Call")
                    await tchan.send(f"Current guilds are: {', '.join(self.calledServers)}")
                self.pending = False
                self.incall = True

        else:
            await ctx.send("There is no Multi-Server Intercom to join. Create one with <>gcall")

    @commands.command()
    async def gleave(self, ctx):
        if ctx.channel in self.calledChannels:
            await ctx.send("You have left")
            self.calledChannels.remove(ctx.channel)
            self.calledServers.remove(ctx.guild.name)
            for tchan in self.calledChannels:
                await tchan.send(f"{ctx.guild}, has left")

            if len(self.calledChannels) <= 1:
                await self.calledChannels[0].send("As the only one left, this Multi-Server Call has been Terminated")
                self.calledChannels.clear()
                self.calledServers.clear()

        else:
            await ctx.send("You are not in the Multi-Server call and therefore can not leave")

    @commands.Cog.listener()
    async def on_message(self, message):


        msgembed2 = discord.Embed(
            title=f"{message.author.display_name} from {message.guild}:",
            description=f"{message.content}",
            color=randint(0, 0xffffff)
        )
            

        if message.author == self.bot.user or message.content.startswith("<>"):
            return
        if self.incall:
            if message.channel in self.calledChannels:
                msgembed2.set_thumbnail(url=message.guild.icon_url)
                if len(message.content) == 0:
                    await message.channel.send("It would seem as though you are trying to add an image. If you want to, please copy the image link then send it")
                    return
                await message.delete()
                if "http" in message.content:
                    for tchan in self.calledChannels:
                        await tchan.send(f"{message.author.display_name} from {message.guild}:\n {message.content}")
                else:
                    for tchan in self.calledChannels:
                        await tchan.send(embed=msgembed2)


class ProfanFilter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    badword = ["fuck", "shit", "bitch", "cum", "nigger"]

    async def regulate(self, msg):
        msg = msg.replace("fuck", "fack")
        msg = msg.replace("shit", "shiz")
        msg = msg.replace("bitch", "beech")
        msg = msg.replace("cum", "excrete my sexual fluid")
        msg = msg.replace("nigger", "black friend")
        return msg
        

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        for sword in self.badword:
            if sword in message.content.lower():
                newmsg = await self.regulate(message.content.lower())
                await message.channel.send(f"{message.author.display_name}: {newmsg}")
                await message.delete()
                return
        



def setup(bot):
    bot.add_cog(Miscgen(bot))
    bot.add_cog(CallMisc(bot))
    bot.add_cog(GCallMisc(bot))
    bot.add_cog(getmentioned(bot))
    bot.add_cog(ProfanFilter(bot))
