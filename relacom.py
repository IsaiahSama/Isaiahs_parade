import discord
from discord import user
from discord.ext import commands, tasks
import asyncio
from random import randint
from relastatus import Relauser, egg, allpets, social_dict, columns
import copy
from saving import Saving
import aiosqlite

veri_emojis = ["✅", "❌"]


class Social(commands.Cog):
    """A list of commands for Social Interactions"""
    # Initializes the bot

    def __init__(self, bot) -> None:
        self.bot = bot
        bot.loop.create_task(self.async_init())
        self.checker = 0

    async def async_init(self):
        if self.checker == 0:
            print("Beginning Social set up")
            await self.setup()
            self.checker += 1

    async def setup(self):
        db = await aiosqlite.connect("IParadeDB.sqlite3")
        await db.execute("""CREATE TABLE IF NOT EXISTS SocialTable(
            USER_ID INTEGER PRIMARY KEY UNIQUE NOT NULL,
            GUILD_ID INTEGER,
            USER_NAME TEXT,
            BF_ID INTEGER,
            SPOUSE_ID INTEGER,
            FRIENDS TEXT,
            PARENTS TEXT,
            CHILDREN TEXT,
            PET_ID INTEGER,
            PET_NICK TEXT,
            PET_EXP INTEGER);""")
        
        await db.commit()
        await db.close()

    @commands.command(brief="Creates a social profile", help="Creates a social proile which will be used for main social commands")
    async def createsocial(self, ctx):
        if await self.get_user(ctx.author.id):
            await ctx.send("You already have a profile. View it with `<>socialprofile` or `<>sp`")
            return

        db = await aiosqlite.connect("IParadeDB.sqlite3")
        await db.execute("INSERT INTO SocialTable (USER_ID, GUILD_ID, USER_NAME, PET_EXP) VALUES (?, ?, ?, ?)", (ctx.author.id, ctx.guild.id, ctx.author.name, 0))
        await db.commit()
        await db.close()
        
        await ctx.send("User Account made Successfully. View with \"<>socialprofile\" or <>sp")


    @commands.command(aliases=["sp"], brief="Views your social profile, or the profile of someone else", help="Used for viewing someone's social profile", usage="optional[@user]")
    async def socialprofile(self, ctx, member: discord.Member=None):
        target = member or ctx.author
        user = await self.get_user(target.id)
        if not user:
            await ctx.send("You don't have an account. Create one with <>socialprofile")
            return

        userbed = discord.Embed(
            title=f"Showing profile for {user['USER_NAME']}",
            description=f"From {self.bot.get_guild(user['GUILD_ID']) or 'Unknown Server'}.",
            color=randint(0, 0xffffff)
        )

        userbed.set_thumbnail(url=ctx.author.avatar_url)
        if user["SPOUSE_ID"]:
            spouse = await self.get_user(user["SPOUSE_ID"])
            if spouse:
                userbed.add_field(name="Lover:", value=f"{spouse['USER_NAME']}")
            else:
                userbed.add_field(name="Lover", value="An Unknown Love")
        else:
            userbed.add_field(name="Lover", value="Single like a Pringle")

        userbed.add_field(name="Number of Friends:", value=f"{len(await self.get_x(user['FRIENDS']))}")

        if user["BF_ID"]:
            best_friend = await self.get_user(user["BF_ID"])
            userbed.add_field(name="Best Friend:", value=f"{best_friend['USER_NAME']}")
        else:
            userbed.add_field(name="Best Friend:", value="No best friend")

        if user["CHILDREN"]:
            children_ids = await self.get_x(user["CHILDREN"])
            children_dicts = [await self.get_user(child_id) for child_id in children_ids if await self.get_user(child_id)]
            child_names = [child["USER_NAME"] for child in children_dicts]
            
            userbed.add_field(name="Parent of:", value=f"{', '.join(child_names)}")
        else:
            userbed.add_field(name="Children:", value="No kids.")

        if user["PARENTS"]:
            parent_ids = await self.get_x(user["PARENTS"])
            parent_dicts = [await self.get_user(parent_id) for parent_id in parent_ids if await self.get_user(parent_id)]
            parent_names = [parent["USER_NAME"] for parent in parent_dicts]
            userbed.add_field(name="Child of:", value=f"{', '.join(parent_names)}")
        else:
            userbed.add_field(name="Child of:", value="None")

        if user["PET_ID"]:
            userbed.add_field(name="Pet exp", value=f"{user['PET_EXP']}")
            userbed.add_field(name="Pet", value=f"{user['PET_NICK']}")


        await ctx.send(embed=userbed)
        return

    # Adding A Friend
    @commands.command(brief="Sends a Role Play friend request", help="Used to request someone to be your friend (Role Play wise)", usage='@user')
    async def friend(self, ctx, member: discord.Member=None):
        if ctx.author == member or not member:
            await ctx.send("I'm glad to see you love yourself")
            return

        user1 = await self.get_user(ctx.author.id)
        user2 = await self.get_user(member.id)

        if not user1 or not user2:
            await ctx.send("One of the two of you don't have an account. Create one with <>createsocial")
            return

        await self.send_request(ctx, member, user1, user2, "Friend", "FRIENDS")


    @commands.command(brief="Shows your friends", help="Shows a max of 25 of your friends")
    async def friends(self, ctx):
        if user:= await self.get_user(ctx.author.id):
            friend_embed = discord.Embed(
                title=f"List of all of {user['USER_NAME']}'s friends",
                color=randint(0, 0xffffff)
            )
            friend_ids = await self.get_x(user["FRIENDS"])
            if not friend_ids:
                await ctx.send("You have... NO friends.")
                return
            
            friend_dicts = [await self.get_user(friend_id) for friend_id in friend_ids if await self.get_user(friend_id)]
            friend_names = [friend["USER_NAME"] for friend in friend_dicts]
            for i, friend in enumerate(list(set(friend_names))[:25]):
                friend_embed.add_field(name=f"Friend {i+1}", value=f"{friend}")

            await ctx.send(embed=friend_embed)

        else:
            await ctx.send("You don't have a social account. Use <>createsocial to create one")

    @commands.command(brief="Sends a love request", help="Requests someone to be your lover", usage="@user")
    async def marry(self, ctx, member:discord.Member):
        if ctx.author == member:
            await ctx.send("I'm glad to see you love yourself")
            return
        
        user1 = await self.get_user(ctx.author.id)
        user2 = await self.get_user(member.id)

        if not user1 or not user2:
            await ctx.send("At least one of you do not have a social profile. Create it with <>createsocial before trying to do stuff like that :flushed:.")
            return
        
        await self.send_request(ctx, member, user1, user2, "lover", "SPOUSE_ID")
 
    @commands.command(brief="Breaks up from your loved one", help="Dumps the person you are in a relationship with")
    async def dump(self, ctx):
        if user:= await self.get_user(ctx.author.id):
            if user["SPOUSE_ID"]:
                user2 = await self.get_user(user["SPOUSE_ID"])
                await self.update_relationship("SPOUSE_ID", 0, user["USER_ID"])
                if not user2:
                    await ctx.send(f"{user['NAME']} is not single")
                    return
                await self.update_relationship("SPOUSE_ID", 0, user2["USER_ID"])
                
                await ctx.send(f"{user['NAME']} and {user2['NAME']} are now no more")
            
            else:
                await ctx.send("You are not in a relationship to leave")
        else:
            await ctx.send("You don't have a social profile. Use <>createsocial to create one.")

    @commands.command(brief="Requests someone to be your best friend", help="Use this to add someone as your one and only best friend", usage="@user")
    async def bestfriend(self, ctx, member: discord.Member):
        if ctx.author == member:
            await ctx.send("I'm glad to see you love yourself")
            return
            
        user1, user2 = await self.get_user(ctx.author.id), await self.get_user(member.id)
        if not user1 or not user2:
            await ctx.send("One of the two of you does not have a profile. Create one with <>createsocial")
            return

        await self.update_relationship("BF_ID", user2["USER_ID"], user["USER_ID"])

        await ctx.send(f"{ctx.author.mention} now considers {member.mention} to be their best friend.")


    @commands.command(brief="Add someone to be your child", help="Invites someone to be your child", usage="@user")
    async def newchild(self, ctx, member: discord.Member):
        if ctx.author == member:
            await ctx.send("Being your own child? I'm not sure, seems illegal doesn't it?")
            return

        user1, user2 = await self.get_user(ctx.author.id), await self.get_user(member.id)

        if not user1 or not user2:
            await ctx.send("One of the two of you does not have a profile. Create one with <>createsocial")
            return
        
        await self.send_request(ctx, member, user1, user2, "Parent", "PARENTS")

    # I WANT TO MAKE PETS. THEREFORE I SHALLLLLLL
    @commands.command(breif="Grants you an egg", help="Grants you an egg.")
    async def getpet(self, ctx):
        if user:= await self.get_user(ctx.author.id):
            if user["PET_ID"]:
                await ctx.send("You already have a pet. View with <>pet")
                return
            else:
                await self.update_relationship("PET_ID", egg.tag, user["USER_ID"])
                if not user["PET_NICK"]:
                    await self.update_relationship("PET_NICK", "egg", user["USER_ID"])
                await ctx.send("CONGRATULATIONS. YOU HAVE RECEIVED AN EGG!!! View with <>pet")
        else:
            await ctx.send("Please create an account first. Use <>help Socials")
            return

    # Pet
    @commands.command(brief="Shows information on your pet", help="Shows information on your current pet")
    async def pet(self, ctx):

        if user:= await self.get_user(ctx.author.id):

            if user["PET_ID"]:

                pet = await self.get_pet_by_id(user["PET_ID"], ctx.channel)
        
                petbed = discord.Embed(
                    title=f"{ctx.author.name}'s pet {user['PET_NICK']}",
                    description=f"{pet.name}: {pet.desc}",
                    color=randint(0, 0xffffff)
                )
                
                petbed.set_thumbnail(url=ctx.author.avatar_url)
                petbed.add_field(name="Type:", value=f"{pet.type}")
                petbed.add_field(name="Amount of Stages", value=f"{pet.stages}")
                petbed.add_field(name="Current Stage", value=f"{pet.stage}")
                petbed.add_field(name="Exp", value=f"{user['PET_EXP']}/{pet.expreq}")
                
                await ctx.send(embed=petbed)
                return
            
        await ctx.send("You don't have pet. Get one with <>getpet.")


    @commands.command(brief="Plays with your pet", help="Plays with your pet for exp. Cooldown: 3 minutes, 20 Seconds")
    @commands.cooldown(1, 200, commands.BucketType.user)
    async def play(self, ctx):
        if user := await self.get_user(ctx.author.id):
            if user["PET_ID"]:
                pet = await self.get_pet_by_id(user["PET_ID"], ctx.channel)
                msg = pet.playmessage
                await ctx.send(f"You play with {user['PET_NICK']}")
                await asyncio.sleep(2)
                await ctx.send(f"{user['PET_NICK']} {msg}")
                await self.update_relationship("PET_EXP", user["PET_EXP"] + 20, user["USER_ID"])
            else:
                await ctx.send("You don't have a pet. Get one with <>getpet")
        
        else:
            await ctx.send("Become one of us with <>createsocial")


    @commands.command(brief="Feeds your pet", help="Feeds your pet for pet exp Cooldown 2 minutes")
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def feed(self, ctx):
        if user:= await self.get_user(ctx.author.id):
            if user["PET_ID"]:
                pet = await self.get_pet_by_id(user["PET_ID"], ctx.channel)
                await ctx.send(f"You feed {user['PET_NICK']}")
                await asyncio.sleep(2)
                await ctx.send(f"{user['PET_NICK']} {pet.feedmsg}")
                await self.update_relationship("PET_EXP", user["PET_EXP"] + 15, user["USER_ID"])
                user["PET_EXP"] += 15
            else:
                await ctx.send("You don't have a pet to feed. Do <>getpet to get one")
        else:
            await ctx.send("You are not a member. Become one with <>createsocial")

    @commands.command(brief="Deletes your pet", help="Gets rid of your pet... for a cost")
    async def delpet(self, ctx, confirm=False):
        if user := await self.get_user(ctx.author):
            if user["PET_ID"]:
                pet = await self.get_pet_by_id(user["PET_ID"], ctx.channel)
                await ctx.send(f"{pet.name} will never forgive you.")
                if not confirm:
                    await ctx.send("Do <>delpet True, to confirm")
                    return
                await ctx.send(f"{pet.name} vanishes with a menacing look, and you get the urge to check your social profile")    
                await self.update_relationship("PET_EXP", randint(50, 250), user["USER_ID"])  
                await self.update_relationship("PET_ID", 0, user["USER_ID"])  
                await self.socialprofile(ctx)
            
            else:
                await ctx.send("You don't even have a pet and want to get rid of it?")
                return
        else:
            await ctx.send("Not a member. Become one with <>createsocial")

    @commands.command(brief="Gives your pet a nickname", help="Give your pet a nickname. Carries on from one pet to the next, until you change it", usage="name")
    async def nickpet(self, ctx,*, name):
        if user:= await self.get_user(ctx.author.id):
            if len(name) >= 15:
                await ctx.send("That name is too long")
                return

            await self.update_relationship("PET_NICK", name, user["USER_ID"])
            await ctx.send(f"Set your Pet's name to {name}")

    @commands.command()
    @commands.is_owner()
    async def save(self, ctx):
        self.updateusers.restart()
        print("Updated profile")

    @commands.command(brief="Changes your profile's guild to the one you are currently in", help="Used to switch your profile's guild to the one you are currently in")
    async def updatesocial(self, ctx):
        if user:= await self.get_user(ctx.author.id):
            await self.update_relationship("GUILD_ID", ctx.guild.id, user["USER_ID"])
            await ctx.send(f"Changed your current guild to {ctx.guild.name}")
        else:
            await ctx.send("You don't even have a profile to update")

    # Functions
    
    async def isuser(self, target):
        for user in self.allusers:
            if user.tag == target.id:
                return True
            
        return False

    async def get_user(self, tag):
        "Queries the database for a user's information. Returns None if nothing is found. Tag is the ID of the user."
        db = await aiosqlite.connect("IParadeDB.sqlite3")
        cursor = await db.execute("SELECT * FROM SocialTable WHERE USER_ID == ?", (tag, ))
        row = await cursor.fetchone()
        await db.close()
        if row:
            return await self.get_user_dict(row)
        return None

    async def get_user_dict(self, row) -> dict:
        "Creates a dictionary out of the tuple provided. Tuple will be a row returned from fetchone(). Returns the newly created dictionary"
        user_dict = {}
        for k in social_dict.keys():
            user_dict[k] = row[columns[k]]
        return user_dict

    async def get_pet_by_id(self, target, channel=None):
        pet = [x for x in allpets if x.tag == target]
        try:
            pet = pet[0]
            return copy.copy(pet)
        except IndexError:
            if not channel: return
            await channel.send("Something went wrong getting your pet")

    async def get_x(self, field) -> list:
        """Takes a string of a list of ids, and converts it into a real list of ids. Returns the new list of integer ids"""
        if not field:
            return []
        list_field = field.split(", ")
        cleaned_up = [x for x in list_field if x]
        return [int(x) for x in cleaned_up]

    async def str_x(self, target_list) -> str:
        """Takes a list of ids, turns each id into a string, then joins on ', '. Returns the new string of ids"""

        stringed_list = [str(target) for target in target_list]
        return ', '.join(stringed_list)

    async def update_relationship(self, field, value, user_id):
        """Used to update a singular relationship field.
        Args: Field - FRIENDS, SPOUSE_ID, BF_ID, PARENTS, CHILDREN
            value - The new value to update the field to
            user_id - The ID of the user who's field is being updated"""
        db = await aiosqlite.connect("IParadeDB.sqlite3")
        await db.execute(f"UPDATE SocialTable SET {field} = ? WHERE USER_ID == ?", (value, user_id))
        await db.commit()
        await db.close()

    async def send_request(self, ctx, member, user1, user2, text, db_term):
        """Function that handles sending and managing requests.\nTakes the ctx, member, both user dictionaries, text and DB term\ntext would be the text that will be displayed. For example: Friend, Spouse\nDB term will be used to index the dictionaries, and must therefore match the name of a field in the database. Returns None"""
        try:
            message = await member.send(f"{user1['USER_NAME']} would like to be your '{text}'. Accept with ✅ or deny with ❌")
        except:
            message = await ctx.send(f"{member.mention}: {user1['USER_NAME']} would like to be your '{text}'. Accept with ✅ or deny with ❌")
            
        await ctx.send("Your request has been sent and will be valid for at most 1 hour.")
        
        for emoji in veri_emojis:
            await message.add_reaction(emoji)

        def check(reaction, user):
            return str(reaction.emoji) in veri_emojis and user == member

        try:
            response = await self.bot.wait_for('reaction_add', check=check, timeout=3600)
        except asyncio.TimeoutError:
            await ctx.send(f"{member.name} has left you high and dry {ctx.author.mention}")
        else:
            emoji = str(response[0].emoji)
            if emoji == veri_emojis[0]:

                for e, user in enumerate([user1, user2]):
                    if not db_term.endswith("ID"):
                        if not user[db_term]:
                            value = f"{[user2, user1][e]['USER_ID']}, "
                        else:
                            value_list = await self.get_x(user[db_term])
                            value_list.append([user2, user1][e]['USER_ID'])
                            value = await self.str_x(value_list)
                    else:
                        value = [user2, user1][e]['USER_ID']

                    await self.update_relationship(db_term, value, user["USER_ID"])
                
                await ctx.send(f"{ctx.author.mention} and {member.mention} are now '{text}'s")
            
            else:
                await ctx.send(f"{member.name} has rejected {ctx.author.mention}'s '{text}'ship")

    async def reget(self, tagtoget):
        for user in self.allusers:
            if tagtoget == user.tag:
                return user

    @tasks.loop(minutes=3.0)
    async def updateusers(self):
        if not self.allusers: return
        await Saving().save("reladata", self.allusers)
        

    async def getpetnames(self):
        for acc in self.allusers:
            if acc.haspet():
                if acc.petnick:
                    x = await self.get_pet_by_id(acc.petid)
                    acc.petnick = x.name

    # Events
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot: return
        if user := await self.get_user(message.author.id):
            if user["PET_ID"]:
                user["PET_EXP"] += 5
                pet = await self.get_pet_by_id(user["PET_ID"], message.channel)
                if user["PET_EXP"] >= pet.expreq and pet.expreq != 0:
                    msg, new_pet = pet.evolve()
                    user["PET_EXP"] = 0
                    await message.channel.send(msg)
                    await self.update_relationship("PET_ID", new_pet.id, user["USER_ID"])
                    if not user["PET_NICK"]:
                        new_pet = await self.get_pet_by_id(user["PET_ID"], message.channel)
                        await self.update_relationship("PET_NICK", new_pet.name, user["USER_ID"])
                await self.update_relationship("PET_EXP", user["PET_EXP"], user["USER_ID"])
                
            else:
                return

def setup(bot):
    bot.add_cog(Social(bot))
