import discord
from discord.ext import commands
import asyncio
import random
from random import randint
from dataclasses import dataclass


class MyHelpCommand(commands.MinimalHelpCommand):

    def get_command_signature(self, command):
        return f"{self.clean_prefix} {command.qualified_name} {command.signature}"


class HelpCom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._originalcom = bot.help_command
        bot.help_command = MyHelpCommand(dm_help=True)
        bot.help_command.cog = self


def setup(bot):
    bot.add_cog(HelpCom(bot))
