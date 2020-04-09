import discord, nekos
from discord.ext import commands

COR = 0xF26DDC

class Nsfw(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_nsfw()
    async def pics(self, ctx, args: str = None):
        possible = [
        'feet', 'yuri', 'trap', 'futanari', 'hololewd', 'lewdkemo',
        'solog', 'feetg', 'cum', 'erokemo', 'les', 'wallpaper', 'lewdk',
        'ngif', 'tickle', 'lewd', 'feed', 'gecg', 'eroyuri', 'eron',
        'cum_jpg', 'bj', 'nsfw_neko_gif', 'solo', 'kemonomimi', 'nsfw_avatar',
        'gasm', 'poke', 'anal', 'slap', 'hentai', 'avatar', 'erofeet', 'holo',
        'keta', 'blowjob', 'pussy', 'tits', 'holoero', 'lizard', 'pussy_jpg',
        'pwankg', 'classic', 'kuni', 'waifu', 'pat', '8ball', 'kiss', 'femdom',
        'neko', 'spank', 'cuddle', 'erok', 'fox_girl', 'boobs', 'random_hentai_gif',
        'smallboobs', 'hug', 'ero', 'smug', 'baka'
        ]
        
        if args is None:
            return await ctx.send('Disponível: ```feet, yuri, trap, futanari, hololewd, lewdkemo,\nsolog, feetg, cum, erokemo, les, lewdk,\nngif, tickle, lewd, feed, gecg, eroyuri, eron,\ncum_jpg, bj, nsfw_neko_gif, solo, kemonomimi,\nnsfw_avatar, gasm, anal, hentai, erofeet, holo, \nketa, blowjob, pussy, tits, holoero, lizard, \npussy_jpg, pwankg, classic, kuni, waifu, femdom,\nspank, erok, fox_girl, boobs, random_hentai_gif,\nsmallboobs, ero, smug, goose, woof```')

        choice = args.lower()
        if not choice in possible:
            return await ctx.send('Digite uma das opções disponíveis!')
        
        embed = discord.Embed(colour=COR)
        embed.set_image(url=nekos.img(choice))
        return await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Nsfw(bot))
