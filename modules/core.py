# # # # # # # # # # # # # # # # # # # # # # # # #
#                                               #
#   These are the core commands for Raphtalia.  #
#   Excluding one of these may have unintend    #
#   consequences.                               #
#   Be careful!                                 #
#                                               #
# # # # # # # # # # # # # # # # # # # # # # # # # 
import discord, os, logging
from discord.ext import commands
from utils.embed import *
from pymongo import MongoClient
from random import choice
#from raphtalia import logger

class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Modules for bot config
        self.modules = [
        'text',
        'adm',
        'images',
        'music',
        'nsfw'
        ]
        self.m_string = ', '.join(self.modules)

        # Database connection
        self.db_client = MongoClient("mongodb+srv://Losty:%402Losty%40@raphtaliabot-nl6k6.gcp.mongodb.net/test?retryWrites=true&w=majority")
        self.db = self.db_client.get_database('guild_db')
        self.collection = self.db.get_collection('guild_collection')

    # Core Commands for Raphtalia
    @commands.command(name='enable',aliases=['ativar'])
    @commands.has_permissions(administrator=True)
    async def enable_group(self, ctx, module = None):
        if module == None or not module in self.modules:
            return await ctx.send(f'Módulos: `{m_string}`.', delete_after=60)
        self.collection.update_one(
            {'_id': ctx.guild.id},
            {'$set': {module: True}}
        )
        return await ctx.send(f'Módulo `{module}` ativado com sucesso.')

    @commands.command(name='disable',aliases=['desativar'])
    @commands.has_permissions(administrator=True)
    async def disable_group(self, ctx, module = None):
        if module is None:
            return await ctx.send(f'Módulos: `{m_string}`.', delete_after=60)
        self.collection.update_one(
            {'_id': ctx.guild.id},
            {'$set': {module: False}}
        )
        return await ctx.send(f'Módulo `{module}` desativado com sucesso.')

    @commands.command(name='extensions')
    @commands.is_owner()
    async def list_extensions(self, ctx):
        extensions = [
            'modules.dev',
            'modules.text',
            'modules.webhook',
            'modules.error_handler',
            'modules.adm',
            'modules.images',
            'modules.nsfw',
            'modules.music',
            'modules.tests',
            'modules.core'
        ]
        return await ctx.send(f'Os modulos são: `{", ".join(extensions)}`')

    @commands.command(aliases=['prefixo'])
    async def prefix(self, ctx, new_prefix : str = None):
        if new_prefix and ctx.guild:
            self.collection.update_one({'_id': ctx.guild.id}, {'$set': {'prefix': new_prefix}})
            return await ctx.send(f'O novo prefixo deste servidor é `{new_prefix}`. Use `{new_prefix}help` para obter ajuda.')
        else:
            prefix = self.collection.find_one({'_id': ctx.guild.id})['prefix']
            return await ctx.send(f'O prefixo deste servidor é `{prefix}`.\nUse `{prefix}help` para obter ajuda.')
        
    @commands.command(aliases=['help'])
    async def ajuda(self, ctx):
        ajuda = embedajuda(ctx.author.mention)
        await ctx.send(ctx.author.mention, embed = ajuda)

    @commands.Cog.listener()
    async def on_message(self, message):
        # _prefix = self.collection.find_one({'_id': message.guild.id})['prefix']
        if message.content.startswith('<@!701798980639785000>'):
            respostas = [
            'Fico pensando por que você está marcando um bot...',
            'Gostou do meu nome, é?',
            'Eu sou um robô, não adianta dar em cima de mim :p'
            ]
            await message.channel.send(choice(respostas))
        
        if 'lindo' in message.content.lower() or 'bonito' in message.content.lower():
            if not message.guild.id == 501807001324617748: return
            bezin = discord.utils.get(await message.channel.webhooks(), name='Bezin')
            if not bezin:
                with open(os.path.join("media", "bezin.png"), 'rb') as avatar:
                    bezin = await message.channel.create_webhook(name='Bezin',avatar=avatar.read())
            return await bezin.send(content='Eu sou Iindo!')
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id != 592178925040435213:
            return
        prefix = self.collection.find_one({'_id': member.guild.id})['prefix']
        welcomeembed = embedwelcome(member, bot, prefix)
        await bot.get_channel(592179994193559573).send(member.mention, embed=welcomeembed)
        for r in member.guild.roles:
            if r.name == 'Newbie':
                return await member.add_roles(r)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Olá mundo! Eu sou {self.bot.user}')
        try:
            await self.bot.change_presence(activity=discord.Game('Visite meu website! raphtalia.kody.mobi'), status=discord.Status.idle)
        except:
            print('Não foi possível carregar as tarefas de segundo plano')

def setup(bot):
    bot.add_cog(Core(bot))