import discord
from discord.ext import commands
from time import sleep

class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)
        sleep(.5)
        await ctx.send(f'Chat limpo por {ctx.author.mention} <:raphNhom:674648257321893940>')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member = None, *, reason='_algum motivo..._'):
        if member == None:
           return  await ctx.send('Por favor mencione um usuário válido.')
        await member.kick(reason=reason)
        await ctx.send(f'{ctx.author.mention} expulsou {member.mention} por {reason}')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member = None, *, reason='_algum motivo..._'):
        if member == None:
           return  await ctx.send('Por favor mencione um usuário válido.')
        await member.ban(reason=reason)
        await ctx.send(f'{ctx.author.mention} baniu {member.mention} por {reason}')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member = None):
        if member == None:
            return await ctx.send('Por favor digite um usuário no formato `nome#discriminador`')
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                return await ctx.send(f'{user.mention} foi desbanido por {ctx.author.mention}')

        return await ctx.send(f'O usuário `{member}` não foi banido.')   

def setup(bot):
    bot.add_cog(Cog(bot))




