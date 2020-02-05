import secret

import discord
import time
import sys

import youtube_dl

from discord.ext import commands, tasks
from random import *

try:
    import cogs.admin
    import cogs.text
    import cogs.music
    import cogs.webhook
    import cogs.errorhandler
    import cogs.messageevents
    import cogs.images
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
    'cogs.images',
    'cogs.imgur'
]

COR = 0xF26DDC
TOKEN = secret.token()
OWNER = secret.owner()

bot = commands.Bot(command_prefix = '>', help_command = None, case_insensitive = True, owner_id = OWNER)
client = discord.Client

@bot.check
async def globally_block_dms(ctx):
    if ctx.guild is None:
        raise commands.NoPrivateMessage
    return ctx.guild is not None

@bot.command()
async def ajuda(message):
    mention_author = '{0.author.mention}'.format(message)
    ajuda=discord.Embed(
        title="Ajuda! <a:blush1:592371658589732874>",
        description="Olá, me chamo Raphtalia e sou um simples bot para discord feito pelo @Losty#5440!\n\nMe convide para o seu servidor! -> https://bit.ly/37RavgH",
        color=COR)
    ajuda.set_footer(text="Siga-me no twitter: twitter.com/KKKBini.")
    ajuda.add_field(name="Argumentos:", value='< > - parâmetro obrigatório.\n[ ] parâmetro opcional.', inline=False)
    ajuda.add_field(
        name="Comandos!",
        value='''
        >ajuda - me faz mostrar esta tela!
        >ping - pong!
        >moeda - jogo uma moeda, será que cai cara ou coroa? 👀
        >diga <frase> - direi o que você me mandar
        >filo <pergunta> - chame a Filo-chan para te responder uma pergunta
        >proibir [palavra] - Qual foi a proibição do governo de hoje?
        >inverter <texto> - inverterei o texto que me mandar
        >some <número> <número> - somarei dois números
        >escolha <opções> - escolherei dentre as opções que mandar
        ''',
        inline=False)

    ajuda.add_field(
        name="Música (pode haver bugs, trabalho em progresso!)",
        value='''
        >join - me faz entrar no canal de voz
        >play <nome ou url da musica> - me faz tocar uma música
        >stop - me faz parar a música\n
        ''',
        inline=False)
    ajuda.add_field(
        name="Comandos de Imagens!",
        value='''
        >avatar [@usuario] - mostro o avatar de um usuário
        >imgur [pesquisa] - pesquiso uma imagem no imgur, deixei em branco para uma aleatória.
        >jojo - isso é uma referência?
        >jojomeme - envio o melhor shitpost sobre jojo
        >meme - envio um meme de baixa qualidade aleatório
        >gato - cansado do seu dia? Vou te enviar um gato fofo para alegrar a vida!
        ''',
        inline=False
    )

    thumb = bot.user.avatar_url
    ajuda.set_thumbnail(url=thumb)

    ajuda.set_image(url='https://coverfiles.alphacoders.com/765/76564.png')
    await message.channel.send(mention_author, embed = ajuda)
    if message.author.id == OWNER:
        owner = discord.Embed(
            title='Comandos de Desenvolvedor: ',
            description='''
            >listemojis - lista os emojis do servidor atual
            >teste - testa se tudo está ok
            >load - carrega um módulo
            >unload - descarrega um módulo
            >reload - recarrega um módulo
            >list_modules - lista os módulos
            >eval - testar código
            ''',
            color=COR
        )
        await message.channel.send(embed = owner)
    else:
        return

@bot.command()
@commands.is_owner()
async def list_modules(ctx):
    await ctx.channel.send(f'Os modulos são: {extensions}')

@bot.event
async def on_ready():
    print(f'\nOlá mundo! Eu sou {bot.user}')

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
    await bot.change_presence(status=discord.Status.idle, activity=game)

def load_modules():
    for extension in extensions:
        try:
            print(f"Carregando módulo: {extension}...")
            bot.load_extension(extension)
        except Exception:
            print(f"Não foi possível carregar o módulo {extension}")

if __name__ == '__main__':
    load_modules()
    change_presence_task.start()
    try:
        bot.run(TOKEN)
    except KeyError:
        print('Váriavel de ambiente não encontrada.')
