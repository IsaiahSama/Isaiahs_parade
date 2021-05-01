import asyncio
import discord
from discord.ext import commands
from random import randint
from battle_functionality import *
from copy import copy

class RPG(commands.Cog):
    """ Contains all Battle based RPG Commands"""
    def __init__(self, bot) -> None:
        self.bot = bot
        bot.loop.create_task(self.async_init())

    async def async_init(self):
        await self.bot.wait_until_ready()
        print("Loaded in")

    players = []

    @commands.command(brief="Used to create a RPG Profile", help="Used to create a profile to be used for the RPG functionality")
    async def createprofile(self, ctx):
        msg = await ctx.send("React with the emoji of the class you want to be:\n🗡️: Warrior\n🏹: Ranger\n📖: Mage")
        for key in class_emojis.keys():
            await msg.add_reaction(key)

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in class_emojis.keys()

        try:
            reaction = await self.bot.wait_for("reaction_add", check=check, timeout=30.0)
        except asyncio.TimeoutError:
            await ctx.send(":x: Took too long. Try again later", delete_after=5)
            await msg.delete()
            return

        chosen_class = class_emojis[str(reaction[0].emoji)]
        player = copy(player_template)
        player["NAME"] = ctx.author.name
        player["PLAYER_ID"] = ctx.author.id

        if chosen_class == "Warrior": chosen_dict = warrior_dict
        elif chosen_class == "Mage": chosen_dict = mage_dict
        elif chosen_class == "Ranger": chosen_dict = ranger_dict
        else: await ctx.send("Something went wrong with the classes"); return

        for k, v in chosen_dict.items():
            player[k] += v
    
        await ctx.send(f"EVERYONE, Welcome {ctx.author.display_name}, our newest {chosen_class}. Type <>quest to start your first quest")
        
        self.players.append(player)

    @commands.command(brief="Used to view your RPG Battle Profile", help="Shows the profile relating to your RPG account once applicable")
    async def profile(self, ctx):
        player, return_message = await self.is_player(ctx.author)
        if return_message:
            await ctx.send(return_message)
            return
        
        embed = discord.Embed(
            title="Showing Profile",
            description=f"Showing {player['NAME']}'s profile",
            color=randint(0, 0xffffff)
        )

        for k, v in player.items():
            embed.add_field(name=k, value=v)

        await ctx.send(embed=embed)

    @commands.command(brief="Used to start a battle quest", help="Used to initiate a fight based quest")
    async def quest(self, ctx):
        player, return_message = await self.is_player(ctx.author)
        if return_message:
            await ctx.send(return_message)
            return 

        await ctx.send(f"Engaging in combat against game_enemy.")
        # await ctx.send(f"{player.__dict__}\nVS\n{game_enemy}")

        game_enemy = handle_enemy_gen(player)
        
        handler = BattleHandler(player, game_enemy)
        
        battle_emojis = handler.get_battle_emojis(player)

        move_set = ""
        
        for k, v in battle_emojis.items():
            move_set += f"\n{v}: {k}"
        
        move_embed = discord.Embed(
            title="BATTLE",
            description=f"PICK YOUR MOVE!!!{move_set}",
            color=randint(0, 0xffffff)
        )

        # msg = f'```{player["NAME"].center(30, "=")}\nHealth:{player["HEALTH"]}\nPower:{player["POWER"]}\nDefense:{player["DEFENSE"]}\n\n{"Enemy".center(30, "=")}\nHealth: {game_enemy["HEALTH"]}\nPower: {game_enemy["POWER"]}\nDefense: {game_enemy["DEFENSE"]}```'

        stat_embed = discord.Embed(
            title="Player VS Enemy",
            description=f"{player['NAME']} VS {game_enemy['NAME']}",
            color=randint(0, 0xffffff)
        )

        stat_embed.add_field(name="NAME", value=player["NAME"], inline=False)
        stat_embed.add_field(name="HEALTH", value=f'{player["HEALTH"]} / {player["MAX_HEALTH"]}')
        stat_embed.add_field(name="POWER", value=player["POWER"])
        stat_embed.add_field(name="DEFENSE", value=player["DEFENSE"])
        stat_embed.add_field(name="NAME", value=game_enemy["NAME"], inline=False)
        stat_embed.add_field(name="HEALTH", value=game_enemy["HEALTH"])
        stat_embed.add_field(name="POWER", value=game_enemy["POWER"])
        stat_embed.add_field(name="DEFENSE", value=game_enemy["DEFENSE"])

        battle = await ctx.send(embed=stat_embed)
        move_message = await ctx.send(embed=move_embed)
        battle_msg = await ctx.send("React above to start")

        for reaction in battle_emojis.keys():
                await move_message.add_reaction(reaction)

        def check(reaction, user):
            return reaction.emoji in battle_emojis.keys() and user == ctx.author

        winner, loser = None, None

        while player["HEALTH"] > 0 and game_enemy["HEALTH"] > 0:

            try:
                reaction = await self.bot.wait_for("reaction_add", timeout=30, check=check)
            except asyncio.TimeoutError:
                await ctx.send(":x: Took too long to pick your move :x:")
                return

            to_send, player, game_enemy = handler.handle(reaction[0].emoji)

            # msg = f'```{player["NAME"].center(30, "=")}\nHealth:{player["HEALTH"]}\nPower:{player["POWER"]}\nDefense:{player["DEFENSE"]}\n\n{"Enemy".center(30, "=")}\nHealth: {game_enemy["HEALTH"]}\nPower: {game_enemy["POWER"]}\nDefense: {game_enemy["DEFENSE"]}```'

            stat_embed = discord.Embed(
            title="Player VS Enemy",
            description=f"{player['NAME']} VS {game_enemy['NAME']}",
            color=randint(0, 0xffffff)
            )

            stat_embed.add_field(name="NAME", value=player["NAME"], inline=False)
            stat_embed.add_field(name="HEALTH", value=f'{player["HEALTH"]} / {player["MAX_HEALTH"]}')
            stat_embed.add_field(name="POWER", value=player["POWER"])
            stat_embed.add_field(name="DEFENSE", value=player["DEFENSE"])
            stat_embed.add_field(name="NAME", value=game_enemy["NAME"], inline=False)
            stat_embed.add_field(name="HEALTH", value=game_enemy["HEALTH"])
            stat_embed.add_field(name="POWER", value=game_enemy["POWER"])
            stat_embed.add_field(name="DEFENSE", value=game_enemy["DEFENSE"])

            await move_message.edit(embed=move_embed)
            await battle.edit(embed=stat_embed)
            
            await battle_msg.edit(content=to_send)
            if "run successful" in to_send.lower():
                break

            await move_message.clear_reactions()
            for battle_reaction in battle_emojis.keys():
                await move_message.add_reaction(battle_reaction)
            
            if player["HEALTH"] < game_enemy["HEALTH"]:
                winner, loser = game_enemy, player
            else:
                winner, loser = player, game_enemy
            
        await ctx.send("Battle over")
        await self.handle_post_battle(ctx, winner, loser, handler)

    async def handle_post_battle(self, ctx, winner, loser, handler):
        if not winner:
            await ctx.send(f"The winner is... No one. Well, get to live to fight another day.")
            return
        if winner.get("TYPE", None):
            loser["LIVES"] -= 1
            if loser["LIVES"] == 0:
                await ctx.send(f"{loser['NAME']} has lost their last life. Goodbye")
                self.players.remove(loser)
            else:
                await ctx.send(f"{loser['NAME']} has lost this fight, and a life. {loser['LIVES']} remain")
        else:
            winner["PARADIANS"] += loser["PARADIANS"]
            winner["EXP"] += loser["EXPGAIN"]
            await ctx.send(f"CONGRATULATIONS, {ctx.author.mention} has defeated {loser['NAME']}, and gained {loser['PARADIANS']} Paradians, and {loser['EXPGAIN']} exp points.")
            if winner["EXP"] >= winner["EXP_FOR_NEXT_LEVEL"]:
                msg, winner = handler.handle_level_up(winner)
                await ctx.send(msg)

    healing = []

    @commands.Cog.listener()
    async def on_message(self, message):
        player, return_message = await self.is_player(message.author)
        if return_message:
            return 

        if player["HEALTH"] < player["MAX_HEALTH"]:
            if player in self.healing: return

            # Regen mechanic. 1 message per 30 seconds increases health by 5
            self.healing.append(player)
            player["HEALTH"] += 5
            await asyncio.sleep(30)
            self.healing.remove(player)

    async def is_player(self, member):
        player = [player for player in self.players if player["PLAYER_ID"] == member.id]
        if not player:
            return None, "Could not find your Account. Create one with <>createprofile"
        else:
            return player[0], None
    

def setup(bot):
    bot.add_cog(RPG(bot))