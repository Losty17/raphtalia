import discord
import time

from discord.ext import commands
from random import choice

global words
words_file = open("./media/words.txt", "r")
words = words_file.readlines()

words_file.close()

def is_empty(anything):
    if anything:
        return False
    else:
        return True

class Webhook(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def filo(self, message, args = None):
        if args is None:
            msg = f'{message.author.mention} o que exatamente eu deveria responder? 🐤'
        else:
            ans = [
            'Sim',
            'Não',
            'Talvez',
            'Não sei',
            'Concordo',
            'Com certeza',
            'Obviamente não',
            'Não posso negar',
            'Não posso afirmar',
            '(Censurado pelo governo)',
            'Com toda certeza que sim',
            'Para de encher o saco e vai capinar um lote, não tô aqui pra te responder'
            ]
            msg = '{0.author.mention} '.format(message) + choice(ans)
        with open("./media/filo.png", 'rb') as avatar:
            filo = await message.channel.create_webhook(name='Filo-chan',avatar=avatar.read())
        await filo.send(content=msg)
        await filo.delete()

    @commands.command(pass_context=True)
    async def proibir(self, ctx, *args):
        if is_empty(args):
            msg = "Hoje o governo proibiu " + choice(words).lower()
        else:
            proibicao = ' '.join(args)
            msg = 'Hoje o governo proibiu ' + proibicao.lower()
        with open("./media/proibiu.jpg", 'rb') as avatar:
            proibiu = await ctx.channel.create_webhook(name='ProibiuBOT',avatar=avatar.read())
        await proibiu.send(content=msg)
        await proibiu.delete()

    @commands.Cog.listener()
    async def on_message(self, message):
        if 'lindo' in message.content.lower():
            with open("media/bezin.png", 'rb') as f:
                bzin = await message.channel.create_webhook(name='Bezin',avatar=f.read())
            await bzin.send(content='Eu sou Iindo!')
            await bzin.delete()

        if 'bonito' in message.content.lower():
            with open("media/bezin.png", 'rb') as f:
                bzin = await message.channel.create_webhook(name='Bezin',avatar=f.read())
            await bzin.send(content='Eu sou bonïto!')
            await bzin.delete()

def setup(bot):
    bot.add_cog(Webhook(bot))
