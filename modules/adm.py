import discord
from discord.ext import commands
from time import sleep

class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['clean'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount : int = None):
        if amount == None or amount < 5 or amount > 100:
            return await ctx.send('Sintaxe: `clear [valor de 5 a 100]`')
        await ctx.channel.purge(limit=amount)
        sleep(.5)
        await ctx.send(f'Chat limpo por {ctx.author.mention} <:raphNhom:674648257321893940>')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member = None, *, reason='_algum motivo..._'):
        if member == None:
           return  await ctx.send('Sintaxe: `kick @Usuário`')
        await member.kick(reason=reason)
        await ctx.send(f'{ctx.author.mention} expulsou {member.mention} por {reason}')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member = None, *, reason='_algum motivo..._'):
        if member == None:
           return  await ctx.send('Sintaxe: `ban @Usuário`')
        await member.ban(reason=reason)
        await ctx.send(f'{ctx.author.mention} baniu {member.mention} por {reason}')

    @commands.command(aliases=['pardon'])
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

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member : discord.Member = None, reason = '_algum motivo_'):
        if member == None:
            return await ctx.send('Sintaxe: `mute @Usuário`')
        for role in member.roles:
            if role.name == 'Silenciado':
                return await ctx.send(f'{member.mention} já está silenciado.')
        roles = []
        for role in ctx.guild.roles:
            roles.append(role.name)
            if role.name == 'Silenciado':
                muteRole = role
                try:
                    await member.add_roles(role)
                    return await ctx.send(f"{ctx.author.mention} silenciou {member.mention} por {reason}")
                except:
                    return await ctx.send('Não fui capaz de silenciar o usuário.')
        if not "Silenciado" in roles:
            overwrite = discord.PermissionOverwrite(send_messages=False)
            newRole = await ctx.guild.create_role(name="Silenciado")

            for channel in ctx.guild.text_channels:
                await channel.set_permissions(newRole, overwrite=overwrite)

            try:
                await member.add_roles(newRole)
                return await ctx.send(f"{ctx.author.mention} silenciou {member.mention} por {reason}")
            except:
                return await ctx.send('Não fui capaz de silenciar o usuário.')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member : discord.Member = None):
        if member == None:
            return await ctx.send('Sintaxe: `unmute @Usuário`')
        roles = []
        for role in member.roles:
            roles.append(role.name)
            if role.name == 'Silenciado':
                try:
                    await member.remove_roles(role)
                    return await ctx.send(f'{member.mention} agora pode falar.')
                except:
                    return await ctx.send('Não fui capaz de remover o silenciamento do usuário')
        if not 'Silenciado' in roles:
            return await ctx.send(f'{member.mention} não foi silenciado.')

def setup(bot):
    bot.add_cog(Cog(bot))