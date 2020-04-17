import discord, nekos

from discord.ext import commands

class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            return await ctx.send('Desculpe, mas é necessário estar em um servidor para utilizar meus comandos.')
        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send('Este comando está desabilitado temporariamente.')
        elif isinstance(error, commands.errors.NSFWChannelRequired):
            return await ctx.send(f'Você so pode usar este comando em um canal NSFW!')
        elif isinstance(error, commands.CheckFailure):
            return await ctx.send('Você não tem permissão para acessar este comando!')
        elif isinstance(error, commands.CommandNotFound):
            return
            #await ctx.send('Desculpe, não consegui encontrar o comando solicitado...')
        elif isinstance(error, commands.errors.CommandInvokeError):
            #await ctx.send(f'Ops, acabei encontrando um erro!\n<@!207947146371006464>```{error}```')
            return

def setup(bot):
    bot.add_cog(Error(bot))