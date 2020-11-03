import discord
from discord.ext import commands
import asyncio
import random
from random import randint
from isaiahball import responses


class delemsg:
    def __init__(self, chan, msgobj):
        self.chan = chan
        self.msgobj = msgobj

    def getobj(self):
        return self.msgobj

class Misc(commands.Cog):
    """Misc commands for Misc uses"""
    def __init__(self, bot):
        self.bot = bot


    delmsg = []
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot: return
        istnce = delemsg(message.channel, message)
        print(f"{message.author}: {message.content}")
        test = [dmsg for dmsg in self.delmsg if dmsg.chan == message.channel]
        if test: self.delmsg.remove(test[0])
        self.delmsg.append(istnce)
        await asyncio.sleep(120)
        try:
            self.delmsg.remove(istnce)
        except ValueError: pass

    @commands.command(brief="Shows a message which has been deleted.", help="Shows a message that has been deleted within the last 2 minutes")
    async def nohide(self, ctx):
        
        for dething in self.delmsg:
            if dething.chan == ctx.channel:
                msg = dething.getobj()
                embed = discord.Embed(
                    title=f"{msg.author.name} thought they could hide from me",
                    description=f"{msg.content}",
                    color=randint(0, 0xffffff)
                )

                obj = await ctx.send(embed=embed)
                await asyncio.sleep(30)
                await obj.delete()
                return

        await ctx.send("No messages for me to reveal")


    # Secret messages
    @commands.command(brief="Like Me... but hidden", help="Sends your message as an embed, but doesn't say who sent it... scary")
    async def hme(self, ctx, *, arg):
        msgembed = discord.Embed(
            title="Hidden user said:",
            description=f"{arg}",
            color=randint(0, 0xffffff)
        )

        await ctx.send(embed=msgembed)
        await ctx.message.delete()

    # Fake deathnote
    @commands.command(brief="A fake <>deathnote command.", help="Like deathnote, but doesn't kick anyone")
    async def fdeathnote(self, ctx, member: discord.Member):
        await ctx.send("***Now that I have my potato chips... you only have 60 seconds to live...***")
        await ctx.send(file=discord.File("images/pchip.gif"))
        await asyncio.sleep(30)
        await ctx.send(f"***30 seconds remain {member.display_name}***")
        await asyncio.sleep(25)
        await ctx.send(f"***It is done... goodbye {member.display_name}. You were pathetic compared to L***")
        await asyncio.sleep(15)
        await ctx.send(f"*Whoops... seems like I have the wrong deathnote :thinking:*")

    @commands.command(brief="Shows the bot's ping", help="Shows the bot's latency")
    async def ping(self, ctx):
        x = round(self.bot.latency * 1000)
        if x <= 100:
            await ctx.send(f"{x}ms. Excellent I daresay")
        elif x >= 101 and x <= 300:
            await ctx.send(f"{x}ms. Not my best but Let's goooo")
        else:
            await ctx.send(f"{x}ms. I don't feel to good, sorry for any delay")

    @commands.command(brief="Sends an emoji but...", help="Enter the name of an emoji to have the bot send it. Example: <>emoji man_bowing", usage="emoji_name")
    async def emoji(self, ctx, arg):
        await ctx.message.delete()
        await ctx.send(f":{arg}:")

    @commands.command(brief="Attempts to find the last time you were pinged.", help="Searches for the last time you were pinged in the last 700 messages. This only picks up @user not role pings")
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

    


    isaiah = 493839592835907594
    def revealcategory(self):
        return random.choice(responses)

    def revealanswer(self,x):
        return random.choice(x)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

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

   


def setup(bot):
    bot.add_cog(Misc(bot))
