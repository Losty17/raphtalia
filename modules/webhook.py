import discord, time, os

from discord.ext import commands
from random import choice

words_file = open(os.path.join('media', 'words.txt'), "r")
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

    @commands.command(pass_context=True, aliases=['8ball'])
    async def filo(self, ctx, args = None):
        if args is None:
            msg = f'{ctx.author.mention} o que exatamente eu deveria responder? 🐤'
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
        msg = choice(ans)
        h = await ctx.channel.webhooks()
        whooks = []
        for wh in h:
            whooks.append(wh.name)
            if wh.name == "Filo-chan":
                proibiu = wh
                return await wh.send(content=msg)
        if not "Filo-chan" in whooks:
            with open(os.path.join("media", "filo.png"), 'rb') as avatar:
                filo = await ctx.channel.create_webhook(name='Filo-chan',avatar=avatar.read())
            await filo.send(content=msg)

    @commands.command(pass_context=True)
    async def proibir(self, ctx, *args):
        if is_empty(args):
            msg = "Hoje o governo proibiu " + choice(words).lower()
        else:
            proibicao = ' '.join(args)
            msg = 'Hoje o governo proibiu ' + proibicao.lower()
        h = await ctx.channel.webhooks()
        whooks = []
        for wh in h:
            whooks.append(wh.name)
            if wh.name == "ProibiuBOT":
                proibiu = wh
                return await wh.send(content=msg)
        if not "ProibiuBOT" in whooks:
            with open(os.path.join("media", "proibiu.jpg"), 'rb') as avatar:
                proibiu = await ctx.channel.create_webhook(name='ProibiuBOT',avatar=avatar.read())
            return await proibiu.send(content=msg)
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if 'lindo' in message.content.lower() or 'bonito' in message.content.lower():
            if not message.guild.id == 501807001324617748:
                return
            msg = 'Eu sou Iindo!'
            h = await message.channel.webhooks()
            whooks = []
            for wh in h:
                whooks.append(wh.name)
                if wh.name == "Bezin":
                    proibiu = wh
                    return await wh.send(content=msg)
            if not "Bezin" in whooks:
                with open(os.path.join("media", "bezin.png"), 'rb') as f:
                    bzin = await message.channel.create_webhook(name='Bezin',avatar=f.read())
                return await bzin.send(content=msg)

def setup(bot):
    bot.add_cog(Webhook(bot))