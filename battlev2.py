import asyncio
from discord.ext import commands
from battle_functionality import *

class RPG(commands.Cog):
    """ Contains all Battle based RPG Commands"""
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

    players = []

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

        chosen_class = self.class_emojis[str(reaction[0].emoji)]

        player = Player(name=ctx.author.name, player_id=ctx.author.id)

        if chosen_class == "Warrior": chosen_dict = warrior_dict
        elif chosen_class == "Mage": chosen_dict = mage_dict
        elif chosen_class == "Ranger": chosen_dict = ranger_dict
        else: await ctx.send("Something went wrong with the classes"); return

        for k, v in chosen_dict.items():
            setattr(player, k.lower(), getattr(player, k.lower()) + v)
    
        await ctx.send(f"EVERYONE, Welcome {ctx.author.display_name}, our newest {chosen_class}")
        
        self.players.clear()
        self.players.append(player)

    async def is_player(self, member):
        player = [player for player in self.players if player.player_id == member.id]
        if not player:
            return None, "Could not find your Account. Create one with <>createprofile"
        else:
            return player[0], None

    @commands.command(brief="Used to view your RPG Battle Profile", help="Shows the profile relating to your RPG account once applicable")
    async def profile(self, ctx):
        player, return_message = await self.is_player(ctx.author)
        if return_message:
            await ctx.send(return_message)
            return

        await ctx.send(player.__dict__)

    @commands.command(brief="Used to start a battle quest", help="Used to initiate a fight based quest")
    async def quest(self, ctx):
        player, return_message = await self.is_player(ctx.author)
        if return_message:
            await ctx.send(return_message)
            return 

        await ctx.send(f"Engaging in combat against enemy.")
        await ctx.send(f"{player.__dict__}\nVS\n{enemy_dict}")
            

def setup(bot):
    bot.add_cog(RPG(bot))