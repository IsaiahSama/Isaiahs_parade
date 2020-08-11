import discord
from discord.ext import commands, tasks
import asyncio
import random
from random import randint
from relastatus import relauser, egg, allpets, petlist
import json
import os
import traceback


class Relamain(commands.Cog):
    # Initializes the bot
    def __init__(self, bot):
        self.bot = bot
        self.updateusers.start()

    # Getting People
    if os.path.exists("relausers.json"):
        with open("relausers.json") as h:
            data = json.load(h)

        tempuser = []
        
        for dictobj in data:
            templist = []
            for v in dictobj.values():
                templist.append(v)
            tempuser.append(templist)

        loadedacc = []
       
        
        for relaperson in tempuser:
            acc = relauser(relaperson[0], relaperson[1], relaperson[2], relaperson[3], relaperson[4],
            relaperson[5], relaperson[6], relaperson[7], relaperson[8], relaperson[9], relaperson[10], relaperson[11],
            relaperson[12])

            loadedacc.append(acc)

        allusers = loadedacc

    else:
        allusers = []

    @commands.command()
    async def createsocial(self, ctx):
        for users in self.allusers:
            if ctx.author.id == users.tag:
                await ctx.send("You already have a profile")
                return True

        nuser = relauser(ctx.guild.name, ctx.author.display_name, ctx.author.id)
        self.allusers.append(nuser)
        await ctx.send("User Account made Successfully. View with \"<>socialprofile\" or <>sp")


    @commands.command()
    async def viewall(self, ctx):
        allembed = discord.Embed(
            title="List of all Users",
            description="Just testing for now",
            color=randint(0, 0xffffff)
        )

        if len(self.allusers) == 0:
            await ctx.send("No users exist as yet")
            return

        for person in self.allusers:
            allembed.add_field(name=f"{person.name}", value=f"Member of {person.guild}")

        await ctx.send(embed=allembed)


    @commands.command(aliases=["sp"])
    async def socialprofile(self, ctx, member: discord.Member=None):
        if member == None:
            x = await self.isuser(ctx.author)
        else:
            x = await self.isuser(member)
        if x:
            if member == None:
                ruser = await self.getuser(ctx.author)
            else:
                ruser = await self.getuser(member)

            userbed = discord.Embed(
                title=f"Showing profile for {ruser.name}",
                description=f"From {ruser.guild}.",
                color=randint(0, 0xffffff)
            )

            userbed.set_thumbnail(url=ctx.author.avatar_url)
            userbed.add_field(name="In Relationship:", value=f"{ruser.rela}")
            if ruser.rela:
                x = await self.reget(ruser.pid)
                userbed.add_field(name="Partner:", value=f"{x.name}")
            userbed.add_field(name="Number of Friends:", value=f"{ruser.friendcount}")
            if ruser.hasbff:
                y = await self.reget(ruser.bfid)
                userbed.add_field(name="Best Friend:", value=f"{y.name}")
            if len(ruser.children) == 0:
                userbed.add_field(name="Parent of:", value=f"None")
            else:
                templist = []
                for item in ruser.children:
                    tuser = await self.reget(item)
                    templist.append(tuser.name)
                userbed.add_field(name="Parent of:", value=f"{', '.join(templist)}")
            if len(ruser.parents) == 0:
                userbed.add_field(name="Child of:", value=f"None")
            else:
                templist = []
                for item in ruser.parents:
                    tuser = await self.reget(item)
                    templist.append(tuser.name)
                userbed.add_field(name="Child of:", value=f"{', '.join(templist)}")

            userbed.add_field(name="Pet exp", value=f"{ruser.petexp}")
            if ruser.haspet():
                pet = await self.getpetid(ruser.petid, ctx.channel)
                userbed.add_field(name="Pet", value=f"{pet.name}")


            await ctx.send(embed=userbed)
            return

        await ctx.send("You do not have a Social Profile. Make one with <>createsocial")


    # Adding A Friend
    @commands.command()
    async def addfriend(self, ctx, member: discord.Member=None):
        if ctx.author == member:
            await ctx.send("I'm glad to see you love yourself")
            return
        if member == None or not await self.isuser(member) or not await self.isuser(ctx.author):
            await ctx.send(f"{member.display_name} does not have a profile. Let them create one with <>createsocial")
            return

        user1 = await self.getuser(ctx.author)
        user2 = await self.getuser(member)

        try: 
            user2.pendingfr
            await ctx.send("User already has a pending request. You must WAIT! >:)")
            return
        except AttributeError:
            await ctx.send("Your request has been sent")

        await member.send(f"{user1.name} would like to be your friend. Accept with <>acceptfr or deny with <>denyfr")

        user2.pendingfr = user1


    @commands.command()
    async def acceptfr(self, ctx):
        yes = await self.isuser(ctx.author)
        if yes:
            user = await self.getuser(ctx.author)
            try:
                user.pendingfr
                await ctx.send(f"Accepting {user.pendingfr.name}'s friend request")
                nf = user.pendingfr
                nf.friendcount += 1
                user.friendcount += 1
                del user.pendingfr

                p1friendlist = list(user.friends)
                p1friendlist.append(nf.tag)
                p2friendlist = list(nf.friends)
                p2friendlist.append(user.tag)
                user.friends = p1friendlist
                nf.friends = p2friendlist

                await ctx.send(f"Successful")
                nfuser = self.bot.get_user(nf.tag)
                await nfuser.send(f"{nf.name}. {user.name} has accepted your Friend Request")

            except AttributeError:
                await ctx.send("You don't have a pending friend request")
        else:
            await ctx.send("You Aren't a user. Become one with <>createsocial")

    @commands.command()
    async def denyfr(self, ctx):
        yes = await self.isuser(ctx.author)
        if yes:
            user = await self.getuser(ctx.author)
            try:
                x = user.pendingfr
                await ctx.send(f"{user.pendingfr.name}'s friend request has been rejected")
                xuser = self.bot.get_user(x.tag)
                await xuser.send(f"{user.name} has rejected your friend request")
                del user.pendingfr

            except AttributeError:
                await ctx.send("You don't have any pending friend requests")

        else:
            await ctx.send("Try creating a profile before rejecting someone. Do so with <>createsocial")


    @commands.command()
    async def showfriends(self, ctx):
        yes = await self.isuser(ctx.author)
        if yes:
            allfrembed = discord.Embed(
                title=f"List of all of {ctx.author.display_name}'s friends",
                color=randint(0, 0xffffff)
            )
            user = await self.getuser(ctx.author)
            for friend in user.friends:
                tuser = await self.reget(friend)
                allfrembed.add_field(name=f"{tuser.name}", value="A friend")

            await ctx.send(embed=allfrembed)

        else:
            await ctx.send("Not a member my good sir. become one with <>createsocial")

    @commands.command()
    async def addlove(self, ctx, member:discord.Member=None):
        """if ctx.author == member:
            await ctx.send("I'm glad to see you love yourself")
            return"""

        if await self.isuser(ctx.author):
            if not await self.isuser(member):
                await ctx.send(f"{member.name} does not have a Social Profile")
                return

            await member.send(f"{ctx.author.name} would like to form a <3 relationship with you. Type <>acceptlove or <>denylove")
            await ctx.send("Your love request has been sent. :thumbsup:")
            target = await self.getuser(member)
            user = await self.getuser(ctx.author)

            target.loverq = user.tag
            print(target.name)
            print(target.loverq)

        else:
            await ctx.send("Do <>createsocial first before jumping into such deep things")

    
    @commands.command()
    async def acceptlove(self, ctx):
        if await self.isuser(ctx.author):
            user = await self.getuser(ctx.author)
            try:
                x = user.loverq

                print(user.name)
                print(x)

                user2 = await self.reget(x)
                user.pname = user2.tag
                user2.pname = user.tag

                mainuser = self.bot.get_user(user.tag)
                await mainuser.send(f"Congratualions. You are now {user2.name}'s lover")
                mainuser.rela = True
                mainuser2 = self.bot.get_user(user2.tag)
                await mainuser2.send(f"Congratualions. You are now {user.name}'s lover")
                mainuser2.rela = True
                del user.loverq

            except AttributeError:
                await ctx.send("You don't have any incoming love requests")

        else:
            await ctx.send("Missing a few steps. Create a Social Profile first with <>createsocial")

    @commands.command()
    async def denylove(self, ctx):
        if await self.isuser(ctx.author):
            user = await self.getuser(ctx.author)
            try:
                del user.loverq
                await ctx.send("Rejected")

            except AttributeError:
                await ctx.send("You don't have any incoming love requests")

        else:
            await ctx.send("Missing a few steps. Create a Social Profile first with <>createsocial")


    @commands.command()
    async def newbff(self, ctx, member: discord.Member=None):
        if ctx.author == member:
            await ctx.send("I'm glad to see you love yourself")
            return
        if await self.isuser(ctx.author) and await self.isuser(member):
            u1 = await self.getuser(ctx.author)
            u2 = await self.getuser(member)

            u2.pendingbf = u1
            await member.send(f"{ctx.author.name} would like to be your best friend")
            await member.send(f"Accept with <>acceptbff or <>denybff to deny")
            await ctx.send("Your Best Friend Request has been sent :thumbsup:")

        else:
            await ctx.send("You or the person you mentioned does not have a profile")

    @commands.command()
    async def acceptbff(self, ctx):
        if await self.isuser(ctx.author):
            user = await self.getuser(ctx.author)
            try:
                x = user.pendingbf
                temp2 = self.bot.get_user(x.tag)
                await ctx.send("Congratulations")
                await temp2.send(f"{user.name} Accepted your best friend request")

                user.bfid = x.tag
                x.bfid = user.tag
                user.hasbff = True
                x.hasbff = True
                del user.pendingbf
            
            except AttributeError:
                await ctx.send("No one has sent you a best friend request")
            
        else:
            await ctx.send("No best friends until you create an account with <>createsocial")

    @commands.command()
    async def denybff(self, ctx):
        if await self.isuser(ctx.author):
            user = await self.getuser(ctx.author)
            try:
                del user.pendingbf
                
                await ctx.send("Rejected")
            
            except AttributeError:
                await ctx.send("No one has sent you a best friend request")
            
        else:
            await ctx.send("No best friends until you create an account with <>createsocial")

    @commands.command()
    async def newchild(self, ctx, member: discord.Member):
        if ctx.author == member:
            await ctx.send("I'm glad to see you love yourself")
            return
        if await self.isuser(ctx.author) and await self.isuser(member):
            user = await self.getuser(ctx.author)
            user2 = await self.getuser(member)
            try:
                user2.pendingpar
                await ctx.send("This person already has a parent request")
                return
            except AttributeError:
                pass

            if len(user2.parents) > 1:
                await ctx.send(f"Sorry to say but, {user2.name} already has 2 parents")
                return

            await member.send(f"Hey. {ctx.author} would like to be your parent. Do <>acceptparent or <>denyparent")
            await ctx.send("Your request has been sent")
            user2.pendingpar = user
        else:
            await ctx.send("You or the person you mentioned, does not have a Social Profile")

    @commands.command()
    async def acceptparent(self, ctx):
        if await self.isuser(ctx.author):
            user = await self.getuser(ctx.author)
            try:
                x = user.pendingpar
                temp2 = self.bot.get_user(x.tag)

                parlist = list(user.parents)
                parlist.append(x.tag)
                user.parents = parlist

                clist = list(x.children)
                clist.append(user.tag)
                x.children = clist

                await ctx.send(f"Successful. Congrats. You are now the child of {x.name}")
                await temp2.send(f"Congratulations. You are now a parent of {user.name}")

            except AttributeError:
                await ctx.send("You don't have any pending parent requests")
                return
        else:
            await ctx.send("You must create a social profile with <>createsocial")

    @commands.command()
    async def denyparent(self, ctx):
        if await self.isuser(ctx.author):
            user = await self.getuser(ctx.author)
            try:
                x = user.pendingpar
                temp1 = self.bot.get_user(x.tag)

                await temp1.send("Your parent request has been denied")
                del user.pendingpar

                await ctx.send("Rejected Successfully")
            
            except AttributeError:
                await ctx.send("You do not have any pending requests")
        
        else:
            await ctx.send("Become one of us with <>createsocial first")

    # I WANT TO MAKE PETS. THEREFORE I SHALLLLLLL
    @commands.command()
    async def getpet(self, ctx):
        if await self.isuser(ctx.author):
            user = await self.getuser(ctx.author)
            if user.haspet():
                await ctx.send("You already have a pet. View with <>pet")
                return
            else:
                user.petid = egg.tag
                await ctx.send("CONGRATULATIONS. YOU HAVE RECEIVED YOUR FIRST PET!!! View with <>pet")
        else:
            await ctx.send("Please create an account first. Use <>help socials")
            return

    # Pet
    @commands.command()
    async def pet(self, ctx):

        if await self.isuser(ctx.author):

            user = await self.getuser(ctx.author)
    
            if user.haspet():

                pett = await self.getpetid(user.petid, ctx.channel)
        
                petbed = discord.Embed(
                    title=f"{ctx.author.name}'s pet",
                    description=f"{pett.name}: {pett.desc}",
                    color=randint(0, 0xffffff)
                )
                
                petbed.set_thumbnail(url=ctx.author.avatar_url)
                petbed.add_field(name="Type:", value=f"{pett.type}")
                petbed.add_field(name="Amount of Stages", value=f"{pett.stages}")
                petbed.add_field(name="Current Stage", value=f"{pett.stage}")
                petbed.add_field(name="Exp", value=f"{user.petexp}/{pett.expreq}")
                
                await ctx.send(embed=petbed)
                return
            
        await ctx.send("You don't have pet. Get one with <>getpet.")

    @commands.command()
    async def updatesocial(self, ctx):
        if await self.isuser(ctx.author):
            user = await self.getuser(ctx.author)
            user.guild = ctx.guild.name
            user.name = ctx.author.display_name
            await ctx.send(f"Changed your current guild to {ctx.guild.name}")

        else:
            await ctx.send("You don't even have a profile to update")

    @commands.command()
    @commands.cooldown(1, 200, commands.BucketType.user)
    async def play(self, ctx):
        if await self.isuser(ctx.author):
            user = await self.getuser(ctx.author)
            if user.haspet():
                pet = await self.getpetid(user.petid, ctx.channel)
                msg = pet.playmessage
                await ctx.send(f"You play with {pet.name}")
                await asyncio.sleep(2)
                await ctx.send(f"{pet.name} {msg}")
                user.petexp += 20
            
            else:
                await ctx.send("You don't have a pet. Get one with <>getpet")
        
        else:
            await ctx.send("Become one of us with <>createsocial")

    @commands.command()
    async def delpet(self, ctx, confirm=False):
        if await self.isuser(ctx.author):
            user = await self.getuser(ctx.author)
            if user.haspet():
                pet = await self.getpetid(user.petid, ctx.channel)
                await ctx.send(f"{pet.name} will never forgive you.")
                if not confirm:
                    await ctx.send("Do <>delpet True, to confirm")
                    return
                if confirm:
                    await ctx.send(f"{pet.name} vanishes with a menacing look, and you get the urge to check your social profile")
                    user.petexp = -30
                    user.petid = None
                    await self.socialprofile(ctx)
            
            else:
                await ctx.send("You don't even have a pet and want to get rid of it?")
                return
        else:
            await ctx.send("Not a member. Become one with <>createsocial")

    @commands.command()
    @commands.is_owner()
    async def save(self, ctx):
        self.updateusers.restart()
        

    # Non Commands
    
    async def isuser(self, target):
        for user in self.allusers:
            if user.tag == target.id:
                return True
            
        return False

    async def getuser(self, target):
        for user in self.allusers:
            if user.tag == target.id:
                return user

    async def getpetid(self, target, channel):
        pett = [x for x in allpets if x.tag == target]
        try:
            pett = pett[0]
            return pett
        except IndexError:
            await channel.send("Something went wrong getting your pet")

    async def reget(self, tagtoget):
        for user in self.allusers:
            if tagtoget == user.tag:
                return user

    @tasks.loop(minutes=2.0)
    async def updateusers(self):
        dumped = []
        for user in self.allusers:

            dumped.append(user.__dict__)

        with open("relausers.json", "w") as f:
            json.dump(dumped, f, indent=4)

        print("Updated Successfully")


    # Events
    @commands.Cog.listener()
    async def on_message(self, message):
        if await self.isuser(message.author):
            user = await self.getuser(message.author)
            if user.haspet():
                user.petexp += 5
                pett = await self.getpetid(user.petid, message.channel)
                if user.petexp >= pett.expreq and pett.expreq != 0:
                    msg, npet = pett.evolve()
                    user.petexp = 0
                    await message.channel.send(msg)
                    user.petid = npet
            else:
                return

        if message.author == self.bot.user:
            return


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # get data from exception
        etype = type(error)
        trace = error.__traceback__

        # the verbosity is how large of a traceback to make
        # more specifically, it's the amount of levels up the traceback goes from the exception source
        verbosity = 4

        # 'traceback' is the stdlib module, `import traceback`.
        lines = traceback.format_exception(etype, error, trace, verbosity)

        # format_exception returns a list with line breaks embedded in the lines, so let's just stitch the elements together
        traceback_text = ''.join(lines)

        # now we can send it to the user
        # it would probably be best to wrap this in a codeblock via e.g. a Paginator
        print(traceback_text)

           

    

def setup(bot):
    bot.add_cog(Relamain(bot))
