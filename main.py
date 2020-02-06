import secret

import discord
import time
import sys

import youtube_dl

from discord.ext import commands, tasks
from random import choice

try:
    import cogs.admin
    import cogs.text
    import cogs.music
    import cogs.webhook
    import cogs.errorhandler
    import cogs.messageevents
    import cogs.imgur
except ImportError as error:
    sys.exit("ERROR: Missing dependency: {0}".format(error))

extensions = [
    'cogs.admin',
    'cogs.music',
    'cogs.text',
    'cogs.webhook',
    'cogs.errorhandler',
    'cogs.messageevents',
    'cogs.imgur'
]


TOKEN = secret.token()
OWNER = secret.owner()

bot = commands.Bot(command_prefix = '>', help_command = None, case_insensitive = True, owner_id = OWNER)
client = discord.Client

# @bot.check
# async def globally_block_dms(ctx):
#     if ctx.guild is None:
#         raise commands.NoPrivateMessage
#     return ctx.guild is not None

@bot.command()
@commands.is_owner()
async def list_modules(ctx):
    await ctx.channel.send(f'Os modulos são: {extensions}')

@bot.event
async def on_ready():
    print(f'\nOlá mundo! Eu sou {bot.user}')
    try:
        change_presence_task.start()
        change_avatar.start()
    except:
        print('Não foi possível carregar as tarefas de segundo plano')

statuses = [
    'Minecraft | >ajuda',
    'League of Legends | >ajuda',
    'Simulador de Dormir | >ajuda',
    'Como cozinhar um humano | >ajuda'
]

@tasks.loop(seconds=120)
async def change_presence_task():
    status = choice(statuses)
    game = discord.Game(status)
    await bot.change_presence(activity=game, status=discord.Status.idle)

avatars = [
    'icon1',
    'icon2',
    'icon3',
    'icon4',
    'icon5',
    'icon6',
    'icon7',
    'icon8'
]
@tasks.loop(hours=1)
async def change_avatar():
    avatar = choice(avatars)
    with open(f'media/avatar/{avatar}.png', 'rb') as b:
        await bot.user.edit(avatar=b.read())

def load_modules():
    for extension in extensions:
        try:
            print(f"Carregando módulo: {extension}...")
            bot.load_extension(extension)
        except Exception:
            print(f"Não foi possível carregar o módulo {extension}")

if __name__ == '__main__':
    load_modules()

    try:
        bot.run(TOKEN)
    except KeyError:
        print('Váriavel de ambiente não encontrada.')
