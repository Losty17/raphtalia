import secret

import discord
import asyncio
import time

import youtube_dl

from discord.ext import commands
from random import randint
from random import choice

COR = 0xF26DDC 
TOKEN = secret.token()
OWNER = 207947146371006464
BOT = secret.bot()

game = discord.Game('digite ">ajuda"!')

songs = asyncio.Queue()
play_next_song = asyncio.Event()

global bot
bot = commands.Bot(command_prefix = '>', help_command = None, case_insensitive = True, owner_id = OWNER)

####

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

def in_guild():
    async def pred(ctx):
        return ctx.guild.id == 501807001324617748

    return commands.check(pred)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

### Cogs

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        
        await channel.connect()
        await ctx.channel.send('Pronta para tocar o bailão!')

    @commands.command()
    async def play(self, ctx, *, url):
        
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Tocando agora: {}!'.format(player.title))

    @commands.command()
    async def stop(self, ctx):

        await ctx.voice_client.disconnect()
        await ctx.channel.send('Saindo... :c')
    
    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("Você não está em um canal de voz :c")
                #raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

class SimpleCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, message):
        mention_author = '{0.author.mention}'.format(message)
        ms = str(int(bot.latency * 1000))
        await message.channel.send(mention_author + ' Pong! Minha latência é de ' + ms + 'ms')

    @commands.command()
    async def ajuda(self, message):
        mention_author = '{0.author.mention}'.format(message)
        ajuda=discord.Embed(
            title="Ajuda! ✨", 
            description="Olá, me chamo Raphtalia e sou um simples bot para discord feito pelo @Losty#5440!\n\nMe convide para o seu servidor! -> https://bit.ly/37RavgH", 
            color=COR)
        ajuda.set_footer(text="Siga-me no twitter: twitter.com/KKKBini.")

        ajuda.add_field(
            name="Comandos", 
            value=">ajuda - me faz mostrar esta tela!\n>moeda - jogo uma moeda, será que cai cara ou coroa? 👀\n>avatar [@usuario] - mostro o avatar de um usuário\n>diga <frase> - direi o que você me mandar\n>filo - chame a Filo-chan para te responder uma pergunta\n>ping - pong!\n",
            inline=False)

        ajuda.add_field(
            name="Música (pode haver bugs, trabalho em progresso!)", 
            value=">join - me faz entrar no canal de voz\n>play <nome ou url da musica> - me faz tocar uma música\n>stop - me faz parar a música\n",
            inline=False)
        
        thumb = bot.user.avatar_url
        ajuda.set_thumbnail(url=thumb)

        ajuda.set_image(url='https://coverfiles.alphacoders.com/765/76564.png')
        if message.author.id == OWNER:
            await message.channel.send('Se esqueceu de novo? :P')
        await message.channel.send(mention_author, embed = ajuda)

    @commands.command()
    async def moeda(self, message):
        mention_author = '{0.author.mention}'.format(message)
        choice = randint(0,1)
        if choice == 0:
            await message.channel.send(mention_author + ' Cara!')
        if choice == 1:
            await message.channel.send(mention_author + ' Coroa!')

    @commands.command(pass_context = True)
    async def diga(self, ctx, *args):
        mesg = ' '.join(args)
        if mesg.lower() == 'pindamonhangaba':
            await ctx.message.channel.send('Achou que eu ia falar? bobinho')
        else:
            await ctx.message.delete()
            await ctx.message.channel.send(mesg)

    @commands.command(pass_context=True)
    async def avatar(self, message, member: discord.Member = None):
        mention_author = '{0.author.mention}'.format(message)
        member = message.author if not member else member

        embed = discord.Embed(colour = COR)
        embed.set_image(url=member.avatar_url)
        await message.channel.send(mention_author, embed = embed)

    @commands.command(pass_context=True)
    async def filo(self, message):
        args = message.message.content.strip('>filo ')
        sup = args + 'a'
        if sup == 'a':
            msg = '{0.author.mention} '.format(message) + 'o que exatamente eu deveria responder? 🐤'
        else:
            ans = ['Sim', 'Não', 'Talvez', 'Não sei', 'Com certeza', 'Não posso afirmar', 'Não posso negar', '(Censurado pelo governo)', 'Obviamente não', 'Com toda certeza que sim', 'Para de encher o saco e vai capinar um lote, não tô aqui pra te responder', 'Concordo']
            msg = '{0.author.mention} '.format(message) + choice(ans)
        with open("filo.png", 'rb') as avatar:
            filo = await message.channel.create_webhook(name='Filo-chan',avatar=avatar.read())
        await filo.send(content=msg)
        await filo.delete()

### ### ###

@bot.event
async def on_ready():
    print('Olá mundo! Eu sou {0}'.format(bot.user))
    await bot.change_presence(
        activity = game, 
        status = discord.Status.idle
        )
@bot.event
@in_guild()
async def on_message(message):
    if bot.user.mentioned_in(message) and not message.content.startswith('>') and message.author != bot.user:
        if message.author.id == OWNER:
            await message.channel.send('Olá, meu pai c:')
        await message.channel.send('Meu prefixo é ">" u.u')
        
    if 'pindamonhangaba' in message.content.lower() and not message.content.startswith('>'):
        await message.channel.send('TALOCO É?')
    
    if 'lindo' in message.content.lower() and not message.content.startswith('>') and message.author != bot.user:
        with open("bezin.png", 'rb') as f:
            bzin = await message.channel.create_webhook(name='Bezin',avatar=f.read())
        await bzin.send(content='Eu sou Iindo!')
        await bzin.delete()
    
    if 'bonito' in message.content.lower() and not message.content.startswith('>') and message.author != bot.user:
        with open("bezin.png", 'rb') as f:
            bzin = await message.channel.create_webhook(name='Bezin',avatar=f.read())
        await bzin.send(content='Eu sou bonïto!')
        await bzin.delete()

    await bot.process_commands(message)

bot.add_cog(Music(bot))
bot.add_cog(SimpleCommands(bot))
bot.run(TOKEN)