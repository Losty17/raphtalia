import discord
import time

import youtube_dl

from discord.ext import commands
from random import randint
from random import choice

global words
words_file = open("./media/words.txt", "r")
words = words_file.readlines()

words_file.close()

COR = 0xF26DDC

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
        mention_author = '{0.author.mention}'.format(message)
        choice = randint(0,1)
        if choice == 0:
            await message.channel.send(mention_author + ' Cara!')
        if choice == 1:
            await message.channel.send(mention_author + ' Coroa!')

    @commands.command(pass_context = True)
    async def diga(self, ctx, args = None):

        if args is not None:
            mesg = args
            if mesg.lower() == 'pindamonhangaba':
                await ctx.message.channel.send('Achou que eu ia falar? bobinho')
            else:
                await ctx.message.delete()
                await ctx.message.channel.send(mesg)
        else:
            await ctx.message.channel.send(f'{ctx.author.mention} o que eu deveria dizer? -.-')

    @commands.command(pass_context=True)
    async def avatar(self, message, member: discord.Member = None):
        mention_author = '{0.author.mention}'.format(message)
        member = message.author if not member else member

        embed = discord.Embed(colour = COR)
        embed.set_image(url=member.avatar_url)
        await message.channel.send(mention_author, embed = embed)

    @commands.command(pass_context=True)
    async def filo(self, message, args = None):
        if args is None:
            msg = '{0.author.mention} '.format(message) + 'o que exatamente eu deveria responder? 🐤'
        else:
            ans = ['Sim', 'Não', 'Talvez', 'Não sei', 'Com certeza', 'Não posso afirmar', 'Não posso negar', '(Censurado pelo governo)', 'Obviamente não', 'Com toda certeza que sim', 'Para de encher o saco e vai capinar um lote, não tô aqui pra te responder', 'Concordo']
            msg = '{0.author.mention} '.format(message) + choice(ans)
        with open("./media/filo.png", 'rb') as avatar:
            filo = await message.channel.create_webhook(name='Filo-chan',avatar=avatar.read())
        await filo.send(content=msg)
        await filo.delete()

    @commands.command(pass_context=True)
    async def proibir(self, ctx, args = None):
        if args is not None:
            msg = 'Hoje o governo proibiu ' + args.lower()
        else:
            msg = "Hoje o governo proibiu " + choice(words).lower()
        with open("./media/proibiu.jpg", 'rb') as avatar:
            proibiu = await ctx.channel.create_webhook(name='ProibiuBOT',avatar=avatar.read())
        await proibiu.send(content=msg)
        await proibiu.delete()

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

def setup(bot):
    bot.add_cog(Text(bot))
    print('Comandos de texto carregados')
