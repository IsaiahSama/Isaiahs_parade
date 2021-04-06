import asyncio
from discord.ext import commands
from discord.ext.commands import bot

class RPG(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        bot.loop.create_task(self.async_init())

    async def async_init(self):
        await self.bot.wait_until_ready()
        print("Loaded in")

    class_emojis = {
        "🗡️": "Warrior",
        "🏹": "Ranger",
        "📖": "Mage"
    }

    @commands.command(brief="Used to create a RPG Profile", help="Used to create a profile to be used for the RPG functionality")
    async def createprofile(self, ctx):
        msg = await ctx.send("React with the emoji of the class you want to be:\n🗡️: Warrior\n🏹: Ranger\n📖: Mage")
        for key in self.class_emojis.keys():
            await msg.add_reaction(key)

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in self.class_emojis.keys()

        try:
            reaction = await self.bot.wait_for("reaction_add", check=check, timeout=30.0)
        except asyncio.TimeoutError:
            await ctx.send(":x: Took too long. Try again later", delete_after=5)
            await msg.delete()
            return
        await ctx.send(f"EVERYONE, Welcome {ctx.author.display_name}, our newest {self.class_emojis[str(reaction[0].emoji)]}")
        

def setup(bot):
    bot.add_cog(RPG(bot))