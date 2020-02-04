import discord
import time

from discord.ext import commands

COR = 0xF26DDC

class Imagens(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def avatar(self, message, member: discord.Member = None):
        if member is None:
            member = message.author
        embed = discord.Embed(colour = COR)
        embed.set_image(url=member.avatar_url)
        await message.channel.send(f'{message.author.mention}', embed = embed)

def setup(bot):
    bot.add_cog(Imagens(bot))
