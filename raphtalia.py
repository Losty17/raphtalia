import discord, time, sys, youtube_dl, json
from discord.ext import commands, tasks
from random import choice
from os import getenv, path
from dotenv import load_dotenv
from time import sleep
import utils.embed as e

try:
    from modules import *
except ImportError as error:
    sys.exit(f'ERROR: Missing dependency: {error}')

extensions = [
    'modules.dev',
    'modules.text',
    'modules.webhook',
    'modules.error_handler',
    'modules.message_events',
    'modules.imgur',
    'modules.adm',
    'modules.images',
    'modules.nsfw',
    'modules.music'
]

load_dotenv()

COR = 0xF26DDC

global prefixxx
prefixxx = getenv('BOT_PREFIX')

bot = commands.Bot(command_prefix=prefixxx,help_command=None,case_insensitive=True,owner_id=int(getenv('BOT_OWNER')))

@bot.event
async def on_member_join(member):
    if member.guild.id != 592178925040435213:
        return
    welcomeembed = e.embedwelcome(member, bot, prefixxx)
    await bot.get_channel(592179994193559573).send(member.mention, embed=welcomeembed)

@bot.command()
@commands.is_owner()
async def modules(ctx):
    modules = ', '.join(extensions)
    await ctx.send(f'Os modulos são: `{modules}`')

@bot.command(aliases=['prefixo'])
async def prefix(ctx):
    await ctx.send(f'O prefixo deste servidor é `{prefixxx}`.\nUse `{prefixxx}help` para obter ajuda.')
    
@bot.command(aliases=['help'])
async def ajuda(ctx):
    ajuda = e.embedajuda(ctx.author.mention)
    await ctx.send(ctx.author.mention, embed = ajuda)

@tasks.loop(seconds=120)
async def change_presence_task():
    status = [
    'Minecraft | .ajuda',
    'League of Legends | .ajuda',
    'Simulador de Dormir | .ajuda',
    'Como cozinhar um humano | .ajuda'
    ]
    change = choice(status)
    game = discord.Game(change)
    await bot.change_presence(activity=game, status=discord.Status.idle)

@tasks.loop(hours=1)
async def change_avatar():
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
    avatar = choice(avatars)
    change = path.join('.', 'media', 'avatar', avatar) + '.png'
    with open(change, 'rb') as a:
        await bot.user.edit(avatar=a.read())
    
def load_modules():
    for e in extensions:
        try:
            print(f"Carregando módulo: {e}...")
            bot.load_extension(e)
        except Exception:
            print(f"Não foi possível carregar o módulo {e}")

@bot.event
async def on_ready():
    print(f'\nOlá mundo! Eu sou {bot.user}')
    try:
        change_presence_task.start()
        #change_avatar.start()
    except:
        print('Não foi possível carregar as tarefas de segundo plano')

if __name__ == "__main__":
    load_modules()
    try:
        bot.run(getenv('BOT_TOKEN'))
    except KeyError:
        print('Váriavel de ambiente não encontrada.')
    