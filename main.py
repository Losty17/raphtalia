import secret

import discord
import time
import sys

import youtube_dl

from discord.ext import commands
from random import *

try:
    import cogs.dev
    import cogs.text
    import cogs.music

except ImportError as error:
    sys.exit("ERROR: Missing dependency: {0}".format(error))

COR = 0xF26DDC
TOKEN = secret.token()
OWNER = secret.owner()

global bot

game = discord.Game('digite ">ajuda"!')

bot = commands.Bot(command_prefix = '>', help_command = None, case_insensitive = True, owner_id = OWNER)

extensions = [
    'cogs.dev',
    'cogs.music',
    'cogs.text'
]

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.NoPrivateMessage):
        await ctx.send('Desculpe, mas é necessário estar em um servidor para utilizar meus comandos.')
    elif isinstance(error, commands.DisabledCommand):
        await ctx.send('Este comando está desabilitado temporariamente.')
    elif isinstance(error, commands.CheckFailure):
        await ctx.send('Você não tem permissão para acessar este comando!')
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send(f'Desculpe, não consegui encontrar o comando solicitado...')

@bot.check
async def globally_block_dms(ctx):
    raise commands.NoPrivateMessage
    return ctx.guild is not None

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if 'bom dia' in message.content.lower():
        await message.channel.send('<:meme:672420428702154763>')
        await message.channel.send('<a:pepeInsane:670473893622054953>')

    if bot.user.mentioned_in(message) and not message.content.startswith('>'):
        if message.author.id == OWNER:
            await message.channel.send('Ola denovo')
        await message.channel.send('Meu prefixo é ">" u.u')

    if 'pindamonhangaba' in message.content.lower() and not message.content.startswith('>'):
        await message.channel.send('TALOCO É?')

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

    await bot.process_commands(message)

@bot.command()
async def ajuda(message):
    mention_author = '{0.author.mention}'.format(message)
    ajuda=discord.Embed(
        title="Ajuda! ✨",
        description="Olá, me chamo Raphtalia e sou um simples bot para discord feito pelo @Losty#5440!\n\nMe convide para o seu servidor! -> https://bit.ly/37RavgH",
        color=COR)
    ajuda.set_footer(text="Siga-me no twitter: twitter.com/KKKBini.")

    ajuda.add_field(
        name="Comandos",
        value=">ajuda - me faz mostrar esta tela!\n>moeda - jogo uma moeda, será que cai cara ou coroa? 👀\n>avatar [@usuario] - mostro o avatar de um usuário\n>diga <frase> - direi o que você me mandar\n>filo - chame a Filo-chan para te responder uma pergunta\n>ping - pong!\n>proibir - Qual foi a proibição do governo de hoje?\n>inverter <texto> - inverterei o texto que me mandar",
        inline=False)

    ajuda.add_field(
        name="Música (pode haver bugs, trabalho em progresso!)",
        value=">join - me faz entrar no canal de voz\n>play <nome ou url da musica> - me faz tocar uma música\n>stop - me faz parar a música\n",
        inline=False)

    thumb = bot.user.avatar_url
    ajuda.set_thumbnail(url=thumb)

    ajuda.set_image(url='https://coverfiles.alphacoders.com/765/76564.png')
    await message.channel.send('Se esqueceu de novo? :P')
    await message.channel.send(mention_author, embed = ajuda)
    if message.author.id == OWNER:
        owner = discord.Embed(
            title='Comandos de Desenvolvedor: ',
            description='>listemojis - lista os emojis do servidor atual\n>teste - testa se tudo está ok',
            color=COR
        )
        await message.channel.send(embed = owner)
    else:
        return

@bot.event
async def on_ready():
    print(f'\nOlá mundo! Eu sou {bot.user}')
    await bot.change_presence(
        activity = game,
        status = discord.Status.idle
        )

def load_modules():
    for extension in extensions:
        try:
            print(f"Carregando módulo: {extension}")
            bot.load_extension(extension)
        except Exception:
            print(f"Não foi possível carregar o módulo {extension}")

if __name__ == '__main__':
    load_modules()
    # bot.loop.create_task(change_presence_task())
    try:
        bot.run(TOKEN)
    except KeyError:
        print('Váriavel de ambiente não encontrada.')
