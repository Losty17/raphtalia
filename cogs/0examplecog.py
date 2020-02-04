import discord
import time

from discord.ext import commands

class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Cog(bot))
