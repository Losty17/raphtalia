import discord, time, random, os
from nekos import textcat, cat
from discord.ext import commands
from utils.embed import neko_img_text

COR = 0xF26DDC

class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def avatar(self, ctx, member: discord.Member = None):
        if member is None:
            if ctx.channel.is_nsfw():
                embed=neko_img_text('nsfw_avatar')
            else:
                embed=neko_img_text('avatar')
        else:
            embed=discord.Embed(colour=0xF26DDC)
            embed.set_image(url=member.avatar_url)
        return await ctx.send(f'{ctx.author.mention}', embed=embed)

    @commands.command(aliases=['gato'])
    async def cat(self, ctx):
        embed = discord.Embed(colour = COR)
        embed.set_image(url=cat())
        await ctx.send(ctx.author.mention, embed=embed)
    
    @commands.command()
    async def neko(self, ctx):
        title = random.choice(('An enemy「猫」appears', 'A wild neko appears!', 'A wild 猫 appears', 'This must be work of an enemy 「猫」'))
        return await ctx.send(embed=neko_img_text('ngif', title, textcat()))

    @commands.command(aliases=['ganso'])
    async def goose(self, ctx):
        return await ctx.send(embed=neko_img_text('goose', textcat()))

    @commands.command(aliases=['dog', 'cão', 'cachorro'])
    async def woof(self, ctx):
        return await ctx.send(embed=neko_img_text('woof', textcat()))

    @commands.command(aliases=['lagarto', 'largato', 'lagartixa'])
    async def lizard(self, ctx):
        return await ctx.send(embed=neko_img_text('lizard', textcat()))

    @commands.command(aliases=['tapa'])
    async def slap(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        title=f'{ctx.author.name} bateu em {member.name}'
        return await ctx.send(embed=neko_img_text('slap', title, textcat()))
    
    @commands.command(aliases=['abraçar'])
    async def hug(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        title=f'{ctx.author.name} abraçou {member.name}'
        return await ctx.send(embed=neko_img_text('hug', title, textcat()))

    @commands.command(aliases=['carinho'])
    async def cuddle(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        title=f'{ctx.author.name} fez carinho em {member.name}'
        return await ctx.send(embed=neko_img_text('cuddle', title, textcat()))
    
    @commands.command(aliases=['acariciar'])
    async def pat(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        title=f'{ctx.author.name} acariciou {member.name}'
        return await ctx.send(embed=neko_img_text('pat', title, textcat()))

    @commands.command(aliases=['cutucar'])
    async def poke(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        title=f'{ctx.author.name} cutucou {member.name}'
        return await ctx.send(embed=neko_img_text('poke', title, textcat()))

    @commands.command(aliases=['idiota'])
    async def baka(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        title=f'B-baka {member.name}!'
        return await ctx.send(embed=neko_img_text('baka', title, textcat()))

    @commands.command(aliases=['beijar'])
    async def kiss(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        elif member == self.bot.user:
            embed = discord.Embed(colour=COR)
            embed.set_image(url='https://i.pinimg.com/originals/50/03/9d/50039d415a087ca8c213eb1337c82ca5.jpg')
            return await ctx.send(ctx.author.mention, embed=embed)
        title=f'{ctx.author.name} beijou {member.name}'
        return await ctx.send(embed=neko_img_text('kiss', title, textcat()))

    @commands.command(aliases=['alimentar'])
    async def feed(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        title=f'{ctx.author.name} alimentou {member.name}'
        return await ctx.send(embed=neko_img_text('feed', title, textcat()))

    @commands.command(aliases=['cocegas'])
    async def tickle(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        title=f'{ctx.author.name} fez cócegas em {member.name}'
        return await ctx.send(embed=neko_img_text('tickle', title, textcat()))
    
    @commands.command()
    async def smug(self, ctx):
        return await ctx.send(embed=neko_img_text('smug'))

    @commands.command(aliases=['pic', 'foto', 'random'])
    async def randompic(self, ctx):
        return await ctx.send(embed=neko_img_text(random.choice(('lizard', 'fox_girl', 'gasm', 'kemonomimi'))))

def setup(bot):
    bot.add_cog(Images(bot))