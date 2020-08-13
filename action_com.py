import discord
from discord.ext import commands
import asyncio
import random
from random import randint
from images import hugs, punches, kisses, slaps, knock, poses, flexes


class Action(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def clown(self, ctx):
        clownbed = discord.Embed(
            title="Worthy of this clown award",
            color=randint(0, 0xffffff)
        )

        clownbed.set_image(url="https://pics.me.me/you-dropped-this-2-clowns-license-hey-55698957.png")

        await ctx.send(embed=clownbed)
    # Pose       

    @commands.command()
    async def pose(self, ctx):
        posemsg = [f"{ctx.author.display_name} is posing on ZA WARUDO",
                f"Look out {ctx.author.display_name} is striking a powerful pose", f"{ctx.author.display_name} has started posing",
                f"Who's posing? {ctx.author.display_name} is.", f"Be careful {ctx.author.display_name} is posing. Looking Good"]

        true_pose = random.choice(poses)
        pose_message = random.choice(posemsg)

        poseuse = discord.Embed(
            title="Is that... a jojo Reference?",
            description=pose_message,
            color=randint(0, 0xffffff)
        )

        poseuse.set_thumbnail(url=ctx.author.avatar_url)
        poseuse.set_image(url=true_pose)

        await ctx.send(embed=poseuse)


    # flexing
    @commands.command()
    async def flex(self, ctx, member: discord.Member=None):
        if member == None:
            member = random.choice(ctx.guild.members)
        flexmsg = [f"{ctx.author.display_name} is flexing on {member.display_name}, K-Kono powa",
                f"I wonder, can {member.display_name} survive being flexed on by {ctx.author.display_name}",
                f"{ctx.author.display_name}'s flexing power is over 9000. Poor {member.display_name}",
                f"Is it just me? or is {ctx.author.display_name} failing to flex on {member.display_name}",
                f"{ctx.author.display_name} is flexing on {member.display_name}, with the power of the world"]

        true_flex = random.choice(flexes)
        flex_message = random.choice(flexmsg)
        file = discord.File(f"poses/{true_flex}", filename=true_flex)
        poseuse = discord.Embed(
            title="Is that... a jojo Reference?",
            description=flex_message,
            color=randint(0, 0xffffff)
        )

        poseuse.set_thumbnail(url=ctx.author.avatar_url)
        poseuse.set_image(url=f"attachment://{true_flex}")

        await ctx.send(file=file, embed=poseuse)

    isaiah = 493839592835907594

    # Hug
    @commands.command()
    async def hug(self, ctx, member: discord.Member=None):
        if member == None:
            member = random.choice(ctx.guild.members)
        embrace = random.choice(hugs)
        if ctx.author.id == 510282144828882944:
            msg = f"{ctx.author.display_name} has given {member.display_name} a loving hug :hatched_chick:"
        elif member.id == 510282144828882944 and ctx.author.id == self.isaiah:
            msg = "Ah Isaiah is hugging Rayln, that's some father-daughter love right there :hatched_chick:"
        elif member.id == 510282144828882944:
            msg = f""":hatched_chick: {member.display_name} is being hugged by {ctx.author.display_name}...
    Does Isaiah-Sama agree with that though?"""

        else:
            msg = f"{ctx.author.display_name} hugs {member.display_name}... Isn't that sweet?"

        file = discord.File(f"images/{embrace}", filename=embrace)
        bumping = discord.Embed(
            title="HUGS!",
            description=f"{msg}",
            color=randint(0, 0xffffff)
        )

        bumping.set_thumbnail(url=self.bot.user.avatar_url)
        bumping.set_image(url=f"attachment://{embrace}")

        await ctx.send(file=file, embed=bumping)
        await ctx.message.delete()


    # Slap
    @commands.command()
    async def slap(self, ctx, member: discord.Member=None):
        hit = random.choice(slaps)
        if member == None:
            member = random.choice(ctx.guild.members)

        file = discord.File(f"images/{hit}", filename=f"{hit}")
        bumping = discord.Embed(
            title="Ouch...",
            description=f"{ctx.author.display_name} slaps {member.display_name}... oh me oh my?",
            color=randint(0, 0xffffff)
        )

        bumping.set_thumbnail(url=self.bot.user.avatar_url)
        bumping.set_image(url=f"attachment://{hit}")

        await ctx.send(file=file, embed=bumping)
        
        await ctx.message.delete()


    # Fist Bump
    @commands.command()
    async def fistbump(self, ctx, member: discord.Member=None):
        bumpfist = random.choice(knock)
        if member == None:
            member = random.choice(ctx.guild.members)
        file = discord.File(f"images/{bumpfist}", filename=bumpfist)
        bumping = discord.Embed(
            title="Fists Have been bumped",
            description=f"{ctx.author.display_name} and {member.display_name} bump fists... Brotherhood",
            color=randint(0, 0xffffff)
        )

        bumping.set_thumbnail(url=self.bot.user.avatar_url)
        bumping.set_image(url=f"attachment://{bumpfist}")

        await ctx.send(file=file, embed=bumping)
        await ctx.message.delete()


    # Punch
    @commands.command()
    async def punch(self, ctx, member: discord.Member=None):
        attack = random.choice(punches)
        if member == None:
            member = random.choice(ctx.guild.members)
        file = discord.File(f"images/{attack}", filename=attack)
        bumping = discord.Embed(
            title="Omae wa mou...",
            description=f"{ctx.author.display_name} gives {member.display_name} a taste of their fist... but... but why?",
            color=randint(0, 0xffffff)
        )

        bumping.set_thumbnail(url=self.bot.user.avatar_url)
        bumping.set_image(url=f"attachment://{attack}")

        await ctx.send(file=file, embed=bumping)
        await ctx.message.delete()


    # kiss
    @commands.command()
    async def kiss(self, ctx, member: discord.Member=None):
        smooch = random.choice(kisses)
        if member == None:
            member = random.choice(ctx.guild.members)
        file = discord.File(f"images/{smooch}", filename=smooch)
        bumping = discord.Embed(
            title="Love has been spread",
            description=f"{member.display_name} is kissed by {ctx.author.display_name}... much love",
            color=randint(0, 0xffffff)
        )

        bumping.set_thumbnail(url=self.bot.user.avatar_url)
        bumping.set_image(url=f"attachment://{smooch}")

        await ctx.send(file=file, embed=bumping)
        await ctx.message.delete()

    # Dance
    @commands.command()
    async def dance(self, ctx):
        embed = discord.Embed(
            title=f"{ctx.author.display_name} is dancing",
            color=randint(0, 0xffffff)
        )

        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.set_image(url="https://media.giphy.com/media/11lxCeKo6cHkJy/giphy.gif")

        await ctx.send(embed=embed)

    # Poke
    pokegifs = ["https://media1.tenor.com/images/573002c649f529f0141f07c740df54ea/tenor.gif?itemid=10271400",
    "https://media.giphy.com/media/PkR8gPgc2mDlrMSgtu/giphy.gif",
    "https://i.pinimg.com/originals/40/54/5c/40545c887023ba16e26f094bdb335271.gif",
    "https://i.pinimg.com/originals/40/54/5c/40545c887023ba16e26f094bdb335271.gif",
    "https://media.giphy.com/media/hRQ6OBek0erPG/giphy.gif",
    "https://media1.tenor.com/images/8fe23ec8e2c5e44964e5c11983ff6f41/tenor.gif?itemid=5600215"]
    @commands.command()
    async def poke(self, ctx, member: discord.Member=None):
        if member == None:
            member = random.choice(ctx.guild.members)

        pokebed = discord.Embed(
            title="Hey... Hey you",
            description=f"{ctx.author.display_name} is poking {member.display_name} for attention. Herro?",
            color=randint(0, 0xffffff)
        )

        pokebed.set_thumbnail(url=ctx.author.avatar_url)
        pokebed.set_image(url=random.choice(self.pokegifs))
        await ctx.message.delete()
        await ctx.send(embed=pokebed)


    # pat
    patgifs = ["https://media1.tenor.com/images/8c1a53522a74129607b870910ac288f9/tenor.gif?itemid=7220650",
    "http://gifimage.net/wp-content/uploads/2017/10/headpat-gif-8.gif",
    "https://i.pinimg.com/originals/45/24/f5/4524f5214e0821f736a4a6e410f6faa0.gif",
    "https://media.giphy.com/media/M3a51DMeWvYUo/giphy.gif",
    "https://thumbs.gfycat.com/PositiveWelloffDeviltasmanian-size_restricted.gif"]
    @commands.command()
    async def pat(self, ctx, member: discord.Member=None):
        if member == None:
            member = random.choice(ctx.guild.members)

        patting = discord.Embed(
            title="Mhm yes... Head rub",
            description=f"{member.display_name} is being gently patted by {ctx.author.display_name}... there there",
            color=randint(0, 0xffffff)
        )

        patting.set_thumbnail(url=ctx.author.avatar_url)
        patting.set_image(url=random.choice(self.patgifs))

        await ctx.send(embed=patting)
        await ctx.message.delete()


    # cry
    @commands.command()
    async def cry(self, ctx):
        crygif = ["https://media1.tenor.com/images/87faf9d8d78a73d65488589ccaff0ac6/tenor.gif?itemid=14065929",
                "https://media.tenor.com/images/8e1148a41d17ec823bbfc7036fa3754e/tenor.gif",
                "https://media1.tenor.com/images/e59bd255f933ab786de2de0eb9b49cb9/tenor.gif?itemid=5012100",
                "https://media1.tenor.com/images/ce52606293142a2bd11cda1d3f0dc12c/tenor.gif?itemid=5184314",
                "https://66.media.tumblr.com/5b4e0848d8080db04dbfedf31a4869e2/tumblr_inline_or4whcrg1z1ueut6r_540.gif"]

        crying = random.choice(crygif)

        thetears = discord.Embed(
            title="Aww...",
            description=f"{ctx.author.display_name} is crying... Will anyone comfort them?",
            color=randint(0, 0xffffff)
        )
        thetears.set_thumbnail(url=ctx.author.avatar_url)
        thetears.set_image(url=f"{crying}")

        await ctx.send(embed=thetears)
        await ctx.message.delete()


    # Barrage
    @commands.command()
    async def barrage(self, ctx, member: discord.Member=None):
        barrageimg = ["https://media1.tenor.com/images/8a87bc787cf5579892d7bfe4e3769901/tenor.gif?itemid=14161814",
                    "http://pa1.narvii.com/6738/346988680e878b4d3ae6e9a3eeb96de7aed69713_00.gif",
                    "http://pa1.narvii.com/5969/1f4843a5df86f2875358f912572b62c245b6bb86_hq.gif",
                    "https://lh3.googleusercontent.com/MynZRQS5UMPTC5dLZJVs9OSAMSgqfu8F3H6uEKPxnPWIv5yp_DKdUkt4y6-2y_qyNmOrOtKzdJKS6Gm5z9kNRWes7WOD2OaLckjakkgdQTuTShZw2aUjNz1H2TrLoXFN-q1aCi0A",
                    "https://media1.tenor.com/images/9747ba71c7edff55b2f8ca0aa8eba0f0/tenor.gif?itemid=14428210"]
        img = random.choice(barrageimg)
        if member == None:
            member = random.choice(ctx.guild.members)
        barrages = discord.Embed(
            title="NOW YOU'VE DONE IT",
            description=f"{member.display_name} is brutally barraged by {ctx.author.display_name}"
        )
        barrages.set_thumbnail(url=ctx.author.avatar_url)
        barrages.set_image(url=f"{img}")

        await ctx.send(embed=barrages)


    # blush
    @commands.command()
    async def blush(self, ctx):
        blushgif = ["https://media.discordapp.net/attachments/722220169480634369/722850078951473202/image0.gif",
                    "https://media.discordapp.net/attachments/722220169480634369/722850079119114310/image1.gif",
                    "https://media.discordapp.net/attachments/722220169480634369/722850079374966924/image2.gif?width=312&height=432"]
        blushing = random.choice(blushgif)

        theblush = discord.Embed(
            title="My oh My",
            description=f"{ctx.author.display_name} is blushing furiously... but I don't recall complimenting them",
            color=randint(0, 0xffffff)
        )

        theblush.set_thumbnail(url=ctx.author.avatar_url)
        theblush.set_image(url=f"{blushing}")

        await ctx.send(embed=theblush)

        await ctx.message.delete()


    # Condescending
    @commands.command()
    async def condescend(self, ctx, member: discord.Member=None):
        if member == None:
            member = random.choice(ctx.guild.members)
        
        judge = ["https://66.media.tumblr.com/a0bfe463ee102f27d0b4cb8828507120/tumblr_pt5q6vmM1h1v2387k_540.png",
        "http://robertcutforth.com/images/condescending.jpg",
        "https://www.fairfaxstatic.com.au/content/dam/images/1/3/7/k/5/v/image.related.articleLeadwide.620x349.goywwo.png/1463632964421.jpg",
        "https://th.bing.com/th/id/OIP.lkV1LvKf31ScNK3JrQaZOwHaHa?pid=Api&rs=1",
        "https://swabulous.files.wordpress.com/2012/10/124.jpg",
        "http://i.imgur.com/mPKgUwT.jpg"]

        descend = discord.Embed(
            title="My oh my",
            description=f"{ctx.author.display_name} is giving {member.display_name} such a nasty look. Why did you do what you did {member.display_name}",
            color=randint(0, 0xffffff)
        )

        descend.set_thumbnail(url=member.avatar_url)
        descend.set_image(url=random.choice(judge))

        await ctx.send(embed=descend)

        await ctx.message.delete()




def setup(bot):
    bot.add_cog(Action(bot))
