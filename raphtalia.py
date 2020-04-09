import discord, time, sys, youtube_dl, json
from discord.ext import commands, tasks
from random import choice
from os import getenv, path
from dotenv import load_dotenv
from time import sleep

load_dotenv()

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
    'modules.nsfw'
]

COR = 0xF26DDC

global prefixxx
prefixxx = getenv('BOT_PREFIX')

bot = commands.Bot(command_prefix=prefixxx,help_command=None,case_insensitive=True,owner_id=int(getenv('BOT_OWNER')))

@bot.event
async def on_member_join(member):
    if member.guild.id != 592178925040435213:
        return
    welcomeembed = discord.Embed(
        title='Tragam as bebidas!', 
        description=f'{member.mention} acabou de chegar!', 
        color=COR)
    welcomeembed.add_field(
        name="<:raphNhom:674648257321893940> Precisa de ajuda?", 
        value='Use o comando /ajuda para acessar meu painel de ajuda!', 
        inline=True)
    welcomeembed.add_field(
        name="<:raphOh:674648256608731176> Siga meu criador nas redes sociais!", 
        value=f'Use o comando `{prefixxx}author` para receber um link direto.', 
        inline=True)
    welcomeembed.add_field(
        name="<:raphPat:674648256529170438> Quer divulgar meu servidor?", 
        value=f'Digite discord para receber o link de convite para meu servidor!', 
        inline=True)
    welcomeembed.set_image(url='https://66.media.tumblr.com/d42fbc38b77d5e93f0dabd666d6fe5aa/tumblr_plyo8ka1yZ1y5sd79o3_500.png')
    welcomeembed.set_author(name=f'{bot.user}', icon_url=bot.user.avatar_url)
    #welcomeembed.set_footer(text=f'A {member.guild.name} agora possui {member.guild.size}')
    await bot.get_channel(592179994193559573).send(member.mention, embed=welcomeembed)

@bot.command()
@commands.is_owner()
async def modules(ctx):
    modules = ', '.join(extensions)
    await ctx.send(f'Os modulos são: `{modules}`')

@bot.command(aliases=['prefixo'])
async def prefix(ctx):
    await ctx.send(f'O prefixo deste servidor é `{prefixxx}`.\nUse `{prefixxx}help` para obter ajuda.')

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
        change_avatar.start()
    except:
        print('Não foi possível carregar as tarefas de segundo plano')

if __name__ == "__main__":
    load_modules()
    try:
        bot.run(getenv('BOT_TOKEN'))
    except KeyError:
        print('Váriavel de ambiente não encontrada.')
