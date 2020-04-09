import discord, time, random, os

from imgurpython import ImgurClient
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

imgurclient = ImgurClient(os.getenv('IMGUR_TOKEN'), os.getenv('IMGUR_SECRET'))

COR = 0xF26DDC

def is_empty(anything):
    if anything:
        return False
    else:
        return True

class Imgur(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def meme(self, ctx):
        items = imgurclient.get_album_images('Kz30J')
        img = random.choice(items).link
        await ctx.send(img)

    @commands.command(aliases=['jjba'])
    async def jojo(self, ctx):
        rand = random.randint(0, 113)
        album = imgurclient.get_album_images('FAmyQ')
        img = album[rand].link
        await ctx.send(img)

    @commands.command(aliases=['jojoshitpost','jjbameme'])
    async def jojomeme(self, ctx):
        rand = random.randint(0, 59)  # 60 results generated per page
        items = imgurclient.subreddit_gallery(subreddit='ShitPostCrusaders', sort='time', window='week', page=0)
        img = items[rand].link
        await ctx.send(img)

    @commands.command()
    async def imgur(self, ctx, *args):
        rand = random.randint(0, 59)  # 60 results generated per page
        if is_empty(args):
            items = imgurclient.gallery(section='hot', sort='viral', page=0, window='day', show_viral=True)
        else:
            query = ' '.join(args)
            items = imgurclient.gallery_search(q=query, advanced=None, sort='viral', window='all', page=0)
        img = items[rand].link
        await ctx.send(img)

def setup(bot):
    bot.add_cog(Imgur(bot))
