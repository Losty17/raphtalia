import asyncio
from asyncio import queues
import discord
import youtube_dl
import shutil
import os
from discord.ext import commands
from discord.utils import get

queues = {}

class DiscordDisco(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        if not discord.opus.is_loaded():
            discord.opus.load_opus('libopus.so')

    @commands.command(pass_contect=True, aliases=['j'])
    async def join(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await ctx.send(f'Já estou no canal {channel}!')
            return
        else:
            voice = await channel.connect()
        await ctx.channel.send(f'Entrando no canal {channel}')

    @commands.command(pass_contect=True, aliases=['l'])
    async def leave(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
            await ctx.channel.send(f'Saindo do canal {channel}')

    @commands.command(aliases=['p', 'pla'])
    async def play(self, ctx, url: str):

        def check_queue():
            Queue_infile = os.path.isdir('./Queue')
            if Queue_infile is True:
                filedir = os.path.abspath(os.path.realpath('Queue'))
                length = len(os.listdir(filedir))
                try:
                    first_file = os.listdir(filedir)[0]
                except:
                    queues.clear()
                    return
                
                PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
                main_location = os.path.dirname(PROJECT_ROOT)

                song_path = os.path.abspath(os.path.realpath('./Queue') + '/' + first_file)
                if length != 0:
                    song_there = os.path.isfile('song.mp3')
                    if song_there:
                        os.remove('./song.mp3')
                    shutil.move(song_path, main_location)
                    for file in os.listdir('./'):
                        if file.endswith('.mp3'):
                            os.rename(file, 'song.mp3')

                    voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: check_queue())
                    voice.source = discord.PCMVolumeTransformer(voice.source)
                    voice.source.volume = 0.1

                else:
                    queues.clear()
                    return
            else:
                queues.clear()

        song_there = os.path.isfile('song.mp3')
        try:
            if song_there:
                os.remove('song.mp3')
                queues.clear()
        except PermissionError:
            await ctx.channel.send('A música ainda está tocando, use >queue para adicionar músicas a fila!')
            return

        Queue_infile = os.path.isdir('./Queue')
        try:
            Queue_folder = './Queue'
            if Queue_infile is True:
                shutil.rmtree(Queue_folder)
        except:
            pass

        async with ctx.typing():
            voice = get(self.bot.voice_clients, guild=ctx.guild)

            ydl_opts = {
                'format': 'bestaudio/best',
                'quiet': True,
                'default_search': 'auto',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            for file in os.listdir('./'):
                if file.endswith('.mp3'):
                    name = file
                    os.rename(file, 'song.mp3')

            voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: check_queue())
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 0.1

            try:
                nname = name.rsplit('-', 2)
                await ctx.send(f'Tocando agora: {nname[0]} - {nname[1]} <:raphOh:674648256608731176>')
            except:
                await ctx.send('A música já vai começar!')

    @commands.command(aliases=['ps'])
    async def pause(self, ctx):

        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            voice.pause()
            await ctx.channel.send('Música pausada!')
        else:
            await ctx.channel.send('Não estou tocando nenhuma música... <:raphGrr:674648255933710346>')

    @commands.command(aliases=['r', 'rs', 'unpause', 'up'])
    async def resume(self, ctx):

        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_paused():

            voice.resume()
            await ctx.channel.send('Retomando a música.')
        else:

            await ctx.channel.send('A música não foi pausada!')

    @commands.command(aliases=['s', 'ski'])
    async def skip(self, ctx):

        voice = get(self.bot.voice_clients, guild=ctx.guild)

        queues.clear()

        if voice and voice.is_playing():
            voice.stop()
            await ctx.channel.send('Tocando a próxima música...')
        else:
            await ctx.channel.send('Nenhuma música na fila.')

    @commands.command(aliases=['q', 'que'])
    async def queue(self, ctx, url: str):
        async with ctx.typing():
            queues = {}
            Queue_infile = os.path.isdir('./Queue')
            if Queue_infile is False:
                os.mkdir('Queue')

            filedir = os.path.abspath(os.path.realpath('./Queue'))
            q_num = len(os.listdir(filedir))
            q_num += 1
            add_queue = True
            while add_queue:
                if q_num in queues:
                    q_num += 1
                else:
                    add_queue = False
                    queues[q_num] = q_num

            queue_path = os.path.abspath(os.path.realpath('.\Queue') + f'\song{q_num}.%(ext)s')

            ydl_opts = {
                'format': 'bestaudio/best',
                'quiet': True,
                'default_search': 'auto',
                'outtmpl': queue_path,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])              

            await ctx.channel.send('Música adicionada à fila! <:raphNhom:674648257321893940>')

    @commands.command(aliases=['stp'])
    async def stop(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected:
            voice.stop()
            await ctx.send('Parando as músicas...')
            os.remove('./song.mp3')
            shutil.rmtree('./Queue')
            queues.clear()
        else:
            await ctx.send('Não estou em um canal de voz...') 

def setup(bot):
    bot.add_cog(DiscordDisco(bot))