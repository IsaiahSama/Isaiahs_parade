from discord.ext import commands
from discord.ext.commands import bot

class Battle(commands.Cog):
    def __init__(self) -> None:
        self.bot = bot
        bot.loop.create_task(self.async_init())

def setup(bot):
    bot.add_cog(Battle(bot))