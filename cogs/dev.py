import discord
from discord.ext import commands

class DevOnly(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def teste(self, ctx):
        print('Tudo ok seu delicia!')
        await ctx.message.add_reaction('👌')

    @commands.command()
    @commands.is_owner()
    async def listemojis(self, ctx):
        print(ctx.guild.name + ' emojis:\n')
        for emoji in ctx.guild.emojis:
            print(str(emoji.id) + ' | ' + emoji.name)
        await ctx.channel.send('os emojis já estão no console')

def setup(bot):
    bot.add_cog(DevOnly(bot))
    print('Comandos de desenvolvedor carregados')
