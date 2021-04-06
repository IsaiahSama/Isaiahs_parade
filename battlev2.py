import asyncio
import discord
from discord.ext import commands
from random import randint
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

    battle_emojis = {
        "⚔️": "Attack",
        "🥤" : "Potion",
        "⛓" : "Ability_1",
        "👹" : "Ability_2",
        "😇" : "Blessing",
        "🏃" : "Run",
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
        # await ctx.send(f"{player.__dict__}\nVS\n{enemy}")

        enemy = Enemy()
        
        embed = discord.Embed(
            title="BATTLE",
            description=f"PICK YOUR MOVE!!!\n{dict(zip(self.battle_emojis.values(), self.battle_emojis.keys()))}",
            color=randint(0, 0xffffff)
        )

        msg = f"""
            ```
            Name:\t\t{player.name}\t\t\t\t\tEnemy
            Health:\t\t{player.health}\t\t\t\t\t{enemy.health}
            Power:\t\t{player.power}\t\t\t\t\t{enemy.power}
            Defense:\t\t{player.defense}\t\t\t\t\t{enemy.defense}```
            """

        battle = await ctx.send(embed=embed, content=msg)

        for reaction in self.battle_emojis.keys():
                await battle.add_reaction(reaction)

        def check(reaction, user):
            return reaction.emoji in self.battle_emojis.keys() and user == ctx.author

        handler = BattleHandler(player, enemy)

        while not player.health < 0 or not enemy["HEALTH"] < 0:

            try:
                reaction = await self.bot.wait_for("reaction_add", timeout=30, check=check)
            except asyncio.TimeoutError:
                await ctx.send(":x: Took too long to pick your move :x:")
                return

            handler.handle(reaction[0].emoji)

            msg = f"""
            ```
            Name:\t\t{player.name}\t\t\t\t\tEnemy
            Health:\t\t{player.health}\t\t\t\t\t{enemy.health}
            Power:\t\t{player.power}\t\t\t\t\t{enemy.power}
            Defense:\t\t{player.defense}\t\t\t\t\t{enemy.defense}```
            """

            await battle.edit(embed=embed, content=msg)

            await battle.clear_reactions()
            for battle_reaction in self.battle_emojis.keys():
                await battle.add_reaction(battle_reaction)


def setup(bot):
    bot.add_cog(RPG(bot))