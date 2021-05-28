import asyncio
import discord
import aiosqlite
from discord.ext import commands
from random import randint
from battle_functionality import *
from copy import copy

class RPG(commands.Cog):
    """Contains the commands for Fight Based RPG"""
    def __init__(self, bot) -> None:
        self.bot = bot
        bot.loop.create_task(self.async_init())
        self.checker = 0

    async def async_init(self):
        if self.checker == 0:
            print("Beginning Battle set up")
            await self.setup()
            self.checker += 1


    async def setup(self):
        # Sets up the database
        async with aiosqlite.connect("IParadeDB.sqlite3") as db:
            await db.execute("""CREATE TABLE IF NOT EXISTS FighterTable (
                PLAYER_ID INTEGER PRIMARY KEY UNIQUE NOT NULL,
                NAME TEXT NOT NULL,
                LIVES INTEGER,
                LEVEL INTEGER,
                TIER INTEGER,
                CLASS TEXT,
                MAX_HEALTH INTEGER,
                HEALTH INTEGER,
                POWER INTEGER,
                DEFENSE INTEGER,
                CRIT_CHANCE INTEGER,
                ABILITY_1 TEXT,
                ABILITY_2 TEXT,
                PARADIANS INTEGER,
                WEAPON TEXT,
                ARMOR TEXT,
                EXP INTEGER,
                EXP_FOR_NEXT_LEVEL INTEGER,
                CRITICAL_CHANCE INTEGER,
                CRITICAL_DAMAGE INTEGER)
                """)

            await db.commit()

        print("Database has been setup")

    @commands.command(brief="Used to create a RPG Profile", help="Used to create a profile to be used for the RPG functionality")
    async def createprofile(self, ctx):
        player, return_message = await self.get_player(ctx.author)
        if not return_message:
            await ctx.send(f"You already have an account with {player['LIVES']} lives")
            return

        msg = await ctx.send("React with the emoji of the class you want to be:\n\n🗡️: `Warrior`\n\n🏹: `Ranger`\n\n📖: `Mage`")
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

        db = await aiosqlite.connect("IParadeDB.sqlite3")

        await db.execute("INSERT INTO FighterTable (PLAYER_ID, NAME, LIVES, LEVEL, TIER, CLASS, MAX_HEALTH, HEALTH, POWER, DEFENSE, CRIT_CHANCE, ABILITY_1, ABILITY_2, PARADIANS, WEAPON, ARMOR, EXP, EXP_FOR_NEXT_LEVEL, CRITICAL_CHANCE, CRITICAL_DAMAGE) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?)", (ctx.author.id, player["NAME"], 4, 1, 1, player["CLASS"], 100, 100, player["POWER"], player["DEFENSE"], player["CRIT_CHANCE"], player["ABILITY_1"], player["ABILITY_2"], 100, player["WEAPON"], player["ARMOR"], 0, 100, 0, 0))
        
        await db.commit()
        await db.close()
        role = discord.utils.get(ctx.guild.roles, name="Parader")
        if role:
            await ctx.author.add_roles(role)

    @commands.command(brief="Provides the menu for all RPG Battle commands", help="Shows the menu which allows user to take part in Battle RPG")
    async def menu(self, ctx):
        player, return_message = await self.get_player(ctx.author)
        if return_message:
            await ctx.send(return_message)
            return

        embed = discord.Embed(
            title=f"Showing Battle Menu for {ctx.author.display_name}",
            color=randint(0, 0xffffff)
        )
        
        def check(reaction, user):
            return str(reaction.emoji) in list(menu_options.keys()) and user == ctx.author
        
        message = await ctx.send(embed=embed)

        for k, v in menu_options.items():
            embed.add_field(name=k, value=v, inline=False)

        for emoji in list(menu_options.keys()):
            await message.add_reaction(emoji)

        await message.edit(embed=embed)

        try:
            reaction = await self.bot.wait_for("reaction_add", check=check, timeout=30)  
        except asyncio.TimeoutError:
            await ctx.send("Took too long to respond")
        else:
            emoji = str(reaction[0].emoji)
            func = menu_options[emoji]

            if func == "profile":
                await self.profile(ctx)
            elif func == "quest":
                await self.quest(ctx)
            else:
                await self.train(ctx)


    @commands.command(brief="Used to view your RPG Battle Profile", help="Shows the profile relating to your RPG account once applicable", aliases=["p"])
    async def profile(self, ctx):
        player, return_message = await self.get_player(ctx.author)
        if return_message:
            await ctx.send(return_message)
            return

        embed = discord.Embed(
            title="Showing Profile",
            description=f"Showing {player['NAME']}'s profile",
            color=randint(0, 0xffffff)
        )

        health_check = 0
        level_check = 0

        for k, v in player.items():
            if "health" in k.lower() and health_check == 0:
                embed.add_field(name="HEALTH", value=f"{v}/{player['MAX_HEALTH']}")
                health_check += 1
                continue
            elif "health" in k.lower(): continue

            if "exp" in k.lower() and level_check == 0:
                embed.add_field(name=k, value=f"{v}/{player['EXP_FOR_NEXT_LEVEL']}")
                level_check += 1
                continue
            elif "exp" in k.lower(): continue

            embed.add_field(name=k, value=v)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.member)
    async def train(self, ctx):
        player, return_message = await self.get_player(ctx.author)
        if return_message:
            await ctx.send(return_message)
            return 

        train_embed = discord.Embed(
            title="Training",
            description=f"What do you want to train?\n💢: `Damage`\n🛡️: `Defense`\n💙: `Health`\n💥: `Crit_Chance`",
            color=randint(0, 0xffffff)
        )

        msg = await ctx.send(embed=train_embed)

        for emoji in train_emojis.keys():
            await msg.add_reaction(emoji)
        
        def check(reaction, user):
            return str(reaction.emoji) in list(train_emojis.keys()) and user == ctx.author

        try:
            reaction = await self.bot.wait_for("reaction_add", check=check, timeout=30)
        except asyncio.TimeoutError:
            await ctx.send(":x:Took too long to respond to me. :x:")
            return

        choice = train_emojis[str(reaction[0].emoji)]

        train_embed.description = f"Training {choice}"
        await msg.edit(embed=train_embed)

        trainHandler = TrainingHandler()

        if choice == "Damage":
            player = await trainHandler.handle_damage(self.bot, ctx, player)
        elif choice == "Defense":
            player = await trainHandler.handle_defense(self.bot, ctx, player)
        elif choice == "Health":
            player = await trainHandler.handle_health(self.bot, ctx, player)
        else:
            player = await trainHandler.handle_crit(self.bot, ctx, player)

        if player["EXP"] >= player["EXP_FOR_NEXT_LEVEL"]:
                msg, player = await self.handle_level_up(player)
                await ctx.send(msg)

        await self.handle_post_training(player)

    @commands.command(brief="Used to start a battle quest", help="Used to initiate a fight based quest")
    async def quest(self, ctx):
        player, return_message = await self.get_player(ctx.author)
        if return_message:
            await ctx.send(return_message)
            return
        
        if player["LEVEL"] < 30:
            await ctx.send("Sorry. You are too weak to do battle quests. Use <>train instead")
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
        await self.handle_post_battle(ctx, winner, loser)

    async def handle_post_battle(self, ctx, winner, loser):
        "Handles the winner and loser functionality"
        if not winner:
            await ctx.send(f"The winner is... No one. Well, get to live to fight another day.")
            return
        if winner.get("TYPE", None):
            loser["LIVES"] -= 1
            if loser["LIVES"] == 0:
                await ctx.send(f"{loser['NAME']} has lost their last life. Goodbye")
                await self.kill_player(loser)
            else:
                await ctx.send(f"{loser['NAME']} has lost this fight, and a life. {loser['LIVES']} remain")
                await self.handle_life_loss(loser)

            human = loser
            
        else:
            winner["PARADIANS"] += loser["PARADIANS"]
            winner["EXP"] += loser["EXPGAIN"]
            await ctx.send(f"CONGRATULATIONS, {ctx.author.mention} has defeated {loser['NAME']}, and gained {loser['PARADIANS']} Paradians, and {loser['EXPGAIN']} exp points.")
            if winner["EXP"] >= winner["EXP_FOR_NEXT_LEVEL"]:
                msg, winner = await self.handle_level_up(winner)
                await ctx.send(msg)
            
            human = winner 
        
        await self.handle_post_changes(human)

    # Player Handling

    async def get_player(self, member):
        "Function used to query the database for a player's information."
        db = await aiosqlite.connect("IParadeDB.sqlite3")

        cursor = await db.execute("SELECT * FROM FighterTable where (PLAYER_ID) == ?", (member.id, ))
        row = await cursor.fetchone()

        await db.close()

        if not row:
            return None, "Could not find your Account. Create one with <>createprofile"
        
        return await self.get_player_dict(row), None

    async def get_player_dict(self, player):
        "Returns a dictionary of the player's database values"
        player_dict = copy(player_template)
        for k in player_template.keys():
            player_dict[k] = player[player_columns[k]]
        
        return player_dict

    # Player Updates

    async def kill_player(self, player) -> None:
        db = await aiosqlite.connect("IParadeDB.sqlite3")
        
        await db.execute("DELETE FROM FighterTable WHERE (PLAYER_ID) == ?", (player["PLAYER_ID"],))
        await db.commit()
        await db.close()

    async def handle_life_loss(self, player) -> None:
        db = await aiosqlite.connect("IParadeDB.sqlite3")

        await db.execute("UPDATE FighterTable SET HEALTH = ?, LIVES = ? WHERE PLAYER_ID == ?", (player['MAX_HEALTH'], player["LIVES"], player["PLAYER_ID"]))
        await db.commit()
        await db.close()

    async def handle_level_up(self, player) -> None:
        msg = ""
        player["LEVEL"] += 1
        msg += f"!!!\n{player['NAME']} is now level {player['LEVEL']}"

        if player["LEVEL"] % 100 == 0 and player["LEVEL"] < 5:
            player["TIER"] += 1
            msg += f"\n!!! {player['NAME']} is now Tier {player['TIER']}"

        player["EXP_FOR_NEXT_LEVEL"] *= 1.6

        db = await aiosqlite.connect("IParadeDB.sqlite3")
        await db.execute("UPDATE FighterTable SET LEVEL = ?, TIER = ?, EXP_FOR_NEXT_LEVEL = ? WHERE PLAYER_ID == ?", (player["LEVEL"], player["TIER"], player["EXP_FOR_NEXT_LEVEL"], player["PLAYER_ID"]))
        await db.commit()
        await db.close()

        return msg, player
        
    async def handle_post_changes(self, player) -> None:
        db = await aiosqlite.connect("IParadeDB.sqlite3")

        await db.execute("UPDATE FighterTable SET EXP = ?, PARADIANS = ?, LIVES = ?, HEALTH = ? WHERE PLAYER_ID == ?", (player["EXP"], player["PARADIANS"], player["LIVES"], player["HEALTH"], player["PLAYER_ID"]))

        await db.commit()
        await db.close()

    async def handle_post_training(self, player) -> None:
        db = await aiosqlite.connect("IParadeDB.sqlite3")

        await db.execute("UPDATE FighterTable SET HEALTH = ?, DEFENSE = ?, POWER = ?, CRIT_CHANCE = ?, EXP = ?, EXP_FOR_NEXT_LEVEL = ?, LEVEL = ? WHERE PLAYER_ID == ?", (player['HEALTH'], player["DEFENSE"], player["POWER"], player["CRIT_CHANCE"], player["EXP"], player["EXP_FOR_NEXT_LEVEL"], player["LEVEL"], player["PLAYER_ID"]))

        await db.commit()
        await db.close()

    # Event

    healing = []

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot: return
        player, return_message = await self.get_player(message.author)
        if return_message:
            return 

        if player["HEALTH"] < player["MAX_HEALTH"]:
            if player in self.healing: return

            # Regen mechanic. 1 message per 30 seconds increases health by 5
            self.healing.append(player)
            player["HEALTH"] += 5

            await self.handle_post_changes(player)

            await asyncio.sleep(30)
            self.healing.remove(player)

    @commands.Cog.listener()
    @commands.coold
    async def on_command_error(error, ctx):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"Take it easy. You're on cooldown for another {error.retry_after} seconds")
            return

def setup(bot):
    bot.add_cog(RPG(bot))