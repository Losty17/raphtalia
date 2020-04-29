# # # # # # # # # # # # # # # # # # # # # # # # #
#                                               #
#   These are the admin commands for guilds.    #
#   It may be enabled or disabled using         #
#   Discord commands.                           #
#                                               #
# # # # # # # # # # # # # # # # # # # # # # # # # 
import discord
from discord.ext import commands
from asyncio import sleep
from pymongo import MongoClient

class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_client = MongoClient("mongodb+srv://Losty:%402Losty%40@raphtaliabot-nl6k6.gcp.mongodb.net/test?retryWrites=true&w=majority")
        self.db = self.db_client.get_database('guild_db')
        self.collection = self.db.get_collection('guild_collection')

    # Checking for guilds, then checking if ADM 
    # module is enabled on the guild
    async def cog_check(self, ctx):
        if ctx.guild is None: raise commands.NoPrivateMessage
        col = self.collection.find_one({'_id': ctx.guild.id})
        if col['adm'] == False:
            raise commands.DisabledCommand
        return col['adm'] == True

    @commands.command(aliases=['clean', 'limpar'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount : int = None):
        if amount == None or amount < 5 or amount > 100:
            return await ctx.send('Sintaxe: `clear [valor de 5 a 100]`')
        await ctx.channel.purge(limit=amount)
        await ctx.send(f'Chat limpo por {ctx.author.mention} <:raphNhom:674648257321893940>')

    @commands.command(aliases=['expulsar'])
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member = None, *, reason='_algum motivo..._'):
        if member == None:
           return  await ctx.send('Sintaxe: `kick @Usuário`')
        await member.kick(reason=reason)
        await ctx.send(f'{ctx.author.mention} expulsou {member.mention} por {reason}')

    @commands.command(aliases=['banir'])
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member = None, *, reason='_algum motivo..._'):
        if member == None:
           return  await ctx.send('Sintaxe: `ban @Usuário`')
        await member.ban(reason=reason)
        await ctx.send(f'{ctx.author.mention} baniu {member.mention} por {reason}')

    @commands.command(aliases=['pardon', 'desbanir', 'perdoar'])
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member = None):
        if member == None:
            return await ctx.send('Sintaxe: `pardon nome#discriminador`. Exemplo: `pardon Losty#5440`.')
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                return await ctx.send(f'{user.mention} foi desbanido por {ctx.author.mention}')

        return await ctx.send(f'O usuário `{member}` não foi banido.')   

    @commands.command(aliases=['silenciar', 'mutar'])
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member : discord.Member = None, duration : int = None, *, reason = '_algum motivo..._',):
        if member == None:
            return await ctx.send('Sintaxe: `mute <@usuário> <tempo> <razão>`')
        # Checks if the user has the silence role
        if discord.utils.get(member.roles, name="Silenciado") is not None:
            return await ctx.send(f'{member.mention} já está silenciado.')

        # Find mute role
        muteRole = discord.utils.get(ctx.guild.roles, name="Silenciado")

        # if mute role exists in server, we add it to the member
        if muteRole is not None:
            try:
                await member.add_roles(muteRole)
                if duration == 0:
                    duration = None
                if duration is not None:
                    await ctx.send(f"{ctx.author.mention} silenciou {member.mention} por {duration} segundos, devido a {reason}")
                    await sleep(duration)
                    await member.remove_roles(muteRole)
                    return await ctx.send(f'{member.mention} pode falar novamente.')
                elif duration is None:
                    return await ctx.send(f"{ctx.author.mention} silenciou {member.mention} por {reason}")
            except:
                return await ctx.send('Não fui capaz de silenciar o usuário.')
        
        # if mute role does not exist in guild we create one
        else:
            overwrite = discord.PermissionOverwrite(send_messages=False)
            muteRole = await ctx.guild.create_role(name="Silenciado")
            for channel in ctx.guild.text_channels:
                await channel.set_permissions(muteRole, overwrite=overwrite)
            try:    
                await member.add_roles(muteRole)
                if duration is not None:
                    await ctx.send(f"{ctx.author.mention} silenciou {member.mention} por {duration} segundos, devido a {reason}")
                    await sleep(duration)
                    await member.remove_roles(muteRole)
                    return await ctx.send(f'{member.mention} pode falar novamente.')
                if duration is None:
                    return await ctx.send(f"{ctx.author.mention} silenciou {member.mention} por {reason}")
            except:
                return await ctx.send('Não fui capaz de silenciar o usuário.')
            
    @commands.command(aliases=['desmutar'])
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member : discord.Member = None):
        if member == None:
            return await ctx.send('Sintaxe: `unmute @Usuário`')
        roles = []
        muteRole = discord.utils.get(member.roles, name="Silenciado")
        if muteRole is not None:
            try:
                await member.remove_roles(muteRole)
                return await ctx.send(f'{member.mention} agora pode falar.')
            except:
                return await ctx.send('Não fui capaz de remover o silenciamento do usuário')
        else:
            return await ctx.send(f'{member.mention} não foi silenciado.')

def setup(bot):
    bot.add_cog(Cog(bot))