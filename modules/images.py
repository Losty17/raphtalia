import discord, time, random, os, nekos
from discord.ext import commands

COR = 0xF26DDC

class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def img(self, ctx, typea: str = None):
        if typea is None:
            return await ctx.send(''' Possibilidades: 
        feet, yuri, trap, futanari, hololewd, lewdkemo,
        solog, feetg, cum, erokemo, les, wallpaper, lewdk,
        ngif, tickle, lewd, feed, gecg, eroyuri, eron,
        cum_jpg, bj, nsfw_neko_gif, solo, kemonomimi, nsfw_avatar,
        gasm, poke, anal, slap, hentai, avatar, erofeet, holo,
        keta, blowjob, pussy, tits, holoero, lizard, pussy_jpg,
        pwankg, classic, kuni, waifu, pat, 8ball, kiss, femdom,
        neko, spank, cuddle, erok, fox_girl, boobs, random_hentai_gif,
        smallboobs, hug, ero, smug, goose, baka, woof
        ''')
        embed = discord.Embed(colour=COR)
        embed.set_image(url=nekos.img(typea))
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def avatar(self, ctx, member: discord.Member = None):
        
        if member is None:
            embed = discord.Embed(title='Random avatar by Nekos.life! uwu',colour = COR)
            embed.set_image(url=nekos.img('avatar'))
        else:
            embed = discord.Embed(title=f'{member.name}\'s avatar!',colour = COR)
            embed.set_image(url=member.avatar_url)
        await ctx.send(f'{ctx.author.mention}', embed = embed)

    @commands.command(aliases=['gato'])
    async def cat(self, ctx):
        embed = discord.Embed(colour = COR)
        embed.set_image(url=nekos.cat())
        await ctx.send(ctx.author.mention, embed=embed)
    
    @commands.command()
    async def neko(self, ctx):
        quote = ('An enemy「猫」appears', 'A wild neko appears!', 'A wild 猫 appears', 'This must be work of an enemy 「猫」')
        embed = discord.Embed(title=f'{random.choice(quote)} {nekos.textcat()}', colour=COR)
        embed.set_image(url=nekos.img('ngif'))
        await ctx.send(embed=embed)

    @commands.command()
    async def goose(self, ctx):
        embed = discord.Embed(title=f'{nekos.textcat()}', colour=COR)
        embed.set_image(url=nekos.img('goose'))
        await ctx.send(embed=embed)

    @commands.command()
    async def woof(self, ctx):
        embed = discord.Embed(title=f'{nekos.textcat()}', colour=COR)
        embed.set_image(url=nekos.img('woof'))
        await ctx.send(embed=embed)

    @commands.command()
    async def slap(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        embed = discord.Embed(title=f'{ctx.author.name} slaps {member.name} | {nekos.textcat()}', colour=COR)
        embed.set_image(url=nekos.img('slap'))
        await ctx.send(embed=embed)
    
    @commands.command()
    async def hug(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        embed = discord.Embed(title=f'{ctx.author.name} hugs {member.name} | {nekos.textcat()}', colour=COR)
        embed.set_image(url=nekos.img('hug'))
        await ctx.send(embed=embed)

    @commands.command()
    async def cuddle(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        embed = discord.Embed(title=f'{ctx.author.name} cuddles {member.name} | {nekos.textcat()}', colour=COR)
        embed.set_image(url=nekos.img('cuddle'))
        await ctx.send(embed=embed)
    
    @commands.command()
    async def pat(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        embed = discord.Embed(title=f'{ctx.author.name} pats {member.name} | {nekos.textcat()}', colour=COR)
        embed.set_image(url=nekos.img('pat'))
        await ctx.send(embed=embed)

    @commands.command()
    async def poke(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        embed = discord.Embed(title=f'{ctx.author.name} pokes {member.name} | {nekos.textcat()}', colour=COR)
        embed.set_image(url=nekos.img('poke'))
        await ctx.send(embed=embed)

    @commands.command()
    async def baka(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        embed = discord.Embed(title=f'B-baka {member.name}! | {nekos.textcat()}', colour=COR)
        embed.set_image(url=nekos.img('baka'))
        await ctx.send(embed=embed)

    @commands.command()
    async def kiss(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        embed = discord.Embed(title=f'{ctx.author.name} kisses {member.name} | {nekos.textcat()}', colour=COR)
        embed.set_image(url=nekos.img('kiss'))
        await ctx.send(embed=embed)

    @commands.command()
    async def feed(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        embed = discord.Embed(title=f'{ctx.author.name} feeds {member.name} | {nekos.textcat()}', colour=COR)
        embed.set_image(url=nekos.img('feed'))
        await ctx.send(embed=embed)
    
def setup(bot):
    bot.add_cog(Images(bot))
