import discord
import time

from discord.ext import commands
from random import choice
from random import randint

def is_empty(anything):
    if anything:
        return False
    else:
        return True

class Text(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def ping(self, ctx):
        mesgedit = await ctx.channel.send('Ping?')
        before = time.monotonic()
        message = await mesgedit.edit(content=f"{ctx.author.mention} Pong!")
        ping = (time.monotonic() - before) * 1000
        await mesgedit.edit(content=f"{ctx.author.mention} Pong!  Minha latência é de `{int(ping)}ms`, a latência da API é de `{int(self.bot.latency * 1000)}ms`")

    @commands.command()
    async def moeda(self, message):
        coin = ['Cara!', 'Coroa!']
        pau = choice(coin)
        await message.channel.send(f'{message.author.mention} {pau}')

    @commands.command(pass_context = True)
    async def diga(self, ctx, *args):
        if is_empty(args):
            await ctx.message.channel.send(f'{ctx.author.mention} o que eu deveria dizer? -.-')
        else:
            mesg = ' '.join(args)
            if mesg.lower() == 'pindamonhangaba':
                await ctx.message.channel.send('Achou que eu ia falar? bobinho')
            else:
                await ctx.message.delete()
                await ctx.message.channel.send(mesg)

    @commands.command()
    async def inverter(self, ctx, *, text: str = None):
        if text is not None:
            to_reverse = text
            await ctx.channel.send(str(to_reverse)[::-1])
        else:
            return

    @commands.command()
    async def escolha(self, ctx, *args):
        if is_empty(args):
            await ctx.channel.send(f'{ctx.author.mention} Quais eram as opções mesmo? ;-;')
        else:
            await ctx.channel.send(choice(args))

    @commands.command()
    async def some(self, ctx, left: int, right: int):
        await ctx.send(left + right)

    @commands.command()
    async def role(self, ctx, *args):
        if is_empty(args):
            await ctx.send('Qual deveria ser o número para rolar?')
        else:
            dice = ''.join(args)
            roll = randint(1, int(dice))
            await ctx.send(f'{ctx.author.mention} {roll}!')
def setup(bot):
    bot.add_cog(Text(bot))
