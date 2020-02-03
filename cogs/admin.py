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

    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx, *, module):
        """Loads a module."""
        try:
            self.bot.load_extension(module)
        except commands.ExtensionError as e:
            await ctx.send(f'{e.__class__.__name__}: {e}')
        else:
            await ctx.send(f'{module} foi carregado com sucesso')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, *, module):
        """Unloads a module."""
        try:
            self.bot.unload_extension(module)
        except commands.ExtensionError as e:
            await ctx.send(f'{e.__class__.__name__}: {e}')
        else:
            await ctx.send(f'{module} foi descarregado com sucesso')

    @commands.group(name='reload', hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, *, module):
        """Reloads a module."""
        try:
            self.bot.reload_extension(module)
        except commands.ExtensionError as e:
            await ctx.send(f'{e.__class__.__name__}: {e}')
        else:
            await ctx.send(f'{module} foi recarregado com sucesso')

def setup(bot):
    bot.add_cog(DevOnly(bot))
    print('Comandos de desenvolvedor carregados')
