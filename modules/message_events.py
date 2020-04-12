import discord
import time

from random import choice
from discord.ext import commands

class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if 'dança' in message.content.lower():
            await message.channel.send('<a:conga:528246551773184000><a:conga:528246551773184000>')

        if '<@!675010654939381785>' in message.content:
            respostas = [
            'Fico pensando por que você está marcando um bot...',
            'Gostou do meu nome, é?',
            'Eu sou um robô, não adianta dar em cima de mim :p',
            'Se quer falar com alguém, fale com o <@!207947146371006464>'
            ]
            await message.channel.send(choice(respostas))

        # if '<@!207947146371006464>' in message.content:
        #     await message.channel.send('Talvez ele esteja ocupado agora. Ou não.')

        if 'pindamonhangaba' in message.content.lower() and not message.content.startswith('.'):
            await message.channel.send('TALOCO É?')

def setup(bot):
    bot.add_cog(Cog(bot))