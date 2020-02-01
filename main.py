import secret

import discord
import asyncio
import time

import youtube_dl

from discord.ext import commands
from random import randint

COR = 0xF26DDC 
TOKEN = secret.token()
OWNER = secret.owner()
BOT = secret.bot()

game = discord.Game('meu prefixo é ">"')

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

    @commands.command()
    async def leave(self, ctx):

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
    async def help(self, message):
        mention_author = '{0.author.mention}'.format(message)
        ajuda = discord.Embed(
            title = "Comandos: ",
            color = COR,
            description = "\n!help \n!teste \n!moeda"
        )
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
    async def say(self, ctx, *args):
        mesg = ' '.join(args)
        if mesg == 'pindamonhangaba':
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

### ### ###

@bot.event
async def on_ready():
    print('Olá mundo! Eu sou {0}'.format(bot.user))
    await bot.change_presence(
        activity = game, 
        status = discord.Status.idle
        )

@bot.event
async def on_message(message):
    if bot.user.mentioned_in(message) and not message.content.startswith('>') and message.author != bot.user:
        await message.channel.send('Meu prefixo é ">" u.u')
    if 'pindamonhangaba' in message.content and not message.content.startswith('>'):
        await message.channel.send('TALOCO É?')

    await bot.process_commands(message)


bot.add_cog(Music(bot))
bot.add_cog(SimpleCommands(bot))
bot.run(TOKEN)