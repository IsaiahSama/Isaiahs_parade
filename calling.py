import discord
from discord.ext import commands
import asyncio
import random
from random import randint
from callclass import CallClass

class Call(commands.Cog):
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
    sincall = []
    
    @commands.command()
    async def intercom(self, ctx):
        if await self.callchk(ctx.channel.id):
            await ctx.send("You are already in a call. To make another one, end this one with <>endcall")
            return
        else:
            callingchan = CallClass(ctx.guild.id, ctx.guild.name, ctx.channel.id, True)
            canjoin = await self.roomavailable()
            if canjoin:
                tojoin = random.choice(canjoin)
                await self.joincall(tojoin, callingchan)
                await ctx.send("Connected")
                chan2 = self.bot.get_channel(tojoin.chan1id)
                await chan2.send("Connected")
            else:
                await ctx.send("A room has been opened. Waiting on someone to join")

            self.sincall.append(callingchan)


    @commands.command()
    async def endcall(self, ctx):
        targobj = await self.callchk(ctx.channel.id)
        if targobj.incall:
            chan1, chan2 = await self.getchans(targobj.chan1id, targobj.chan2id)
            await chan1.send("Disconnected")
            await chan2.send("Disconnected")
            guild2 = await self.callchk(targobj.chan2id)
            self.sincall.remove(targobj)
            self.sincall.remove(guild2)
        else:
            await ctx.send("You aren't in a call to leave")

    async def callchk(self, id):
        for guild in self.sincall:
            if id == guild.chan1id:
                return guild
        
        return False

    async def roomavailable(self):
        available = [x for x in self.sincall if x.pending]
        return available

    async def joincall(self, obj1, obj2):
        callist = [obj1, obj2]
        for objt in callist:
            objt.pending = False
            objt.incall = True
        
        obj1.chan2id, obj2.chan2id= obj2.chan1id, obj1.chan1id

    async def getchans(self, chan1, chan2):
        chan1 = self.bot.get_channel(chan1)
        chan2 = self.bot.get_channel(chan2)
        return chan1, chan2

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author == self.bot.user:
            return


        obj1 = await self.callchk(message.channel.id)
        if not obj1:
            return

        if obj1.incall:
            _, chan2 = await self.getchans(obj1.chan1id, obj1.chan2id)
            await chan2.send(f"{message.author.display_name}: {message.content}")

class GroupCall(commands.Cog):
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


def setup(bot):
    bot.add_cog(Call(bot))
    bot.add_cog(GroupCall(bot))
