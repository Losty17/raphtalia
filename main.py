import discord
import asyncio
import time
from discord.ext import commands
from random import randint
import secret

COR = 0xF26DDC 
TOKEN = secret.token()
OWNER = secret.owner()
BOT = secret.bot()

game = discord.Game('my prefix is "!"')

global bot
bot = commands.Bot(command_prefix = '!', help_command = None, case_insensitive = True, owner_id = OWNER)

@bot.event
async def on_ready():
    print('Olá Mundo!')
    await bot.change_presence(
        activity = game, 
        status = discord.Status.idle
        )

@bot.event
async def on_message(message):
    if bot.user.mentioned_in(message) and not message.content.startswith('!') and message.author != bot.user:
        await message.channel.send('Meu prefixo é "!" u.u')
    if 'pindamonhangaba' in message.content and not message.content.startswith('!'):
        await message.channel.send('TALOCO É?')

    await bot.process_commands(message)

@bot.command(pass_context=True)
async def ping(message):
    mention_author = '{0.author.mention}'.format(message)
    ms = str(int(bot.latency * 1000))
    await message.channel.send(mention_author + ' Pong! Minha latência é de ' + ms + 'ms')

@bot.command()
async def help(message):
    mention_author = '{0.author.mention}'.format(message)
    ajuda = discord.Embed(
        title = "Comandos: ",
        color = COR,
        description = "\n!help \n!teste \n!moeda"
    )
    await message.channel.send(mention_author, embed = ajuda)

@bot.command()
async def moeda(message):
    mention_author = '{0.author.mention}'.format(message)
    choice = randint(0,1)
    if choice == 0:
        await message.channel.send(mention_author + ' Cara!')
    if choice == 1:
        await message.channel.send(mention_author + ' Coroa!')

@bot.command(pass_context = True)
async def say(ctx, *args):
    mesg = ' '.join(args)
    if mesg == 'pindamonhangaba':
        await ctx.message.channel.send('Achou que eu ia falar? bobinho')
    else:
        await ctx.message.delete()
        await ctx.message.channel.send(mesg)

bot.run(TOKEN)