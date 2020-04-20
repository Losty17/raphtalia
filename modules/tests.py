import discord, os, asyncio
from discord.ext import commands
from pymongo import MongoClient

##

db_client = MongoClient("mongodb+srv://Losty:%402Losty%40@raphtaliabot-nl6k6.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = db_client.get_database('guild_db')
avatar_collection = db.get_collection('avatar_collection')

##

class Tests(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def profile(self, ctx, member : discord.Member = None):
        if member is None:
            try:
                avatar_collection.insert_one({
                    '_id'     : ctx.author.id,
                    'name'    : ctx.author.name,
                    'bio'     : 'default',
                    'backdrop': 'default',
                })
            except:
                pass
            avatar = ctx.author.avatar_url
            get = avatar_collection.find_one({'_id': ctx.author.id})    
        else:
            avatar = member.avatar_url
            get = avatar_collection.find_one({'_id': member.id})
            if get is None:
                return await ctx.send('Usuário não encontrado')
            
        # Get bio from DB
        if get['bio'] == 'default':
            bio = 'AlMEIDA'
        else:
            bio = get['bio']

        # Get image from DB
        if get['backdrop'] == 'default':
            image = 'https://images5.alphacoders.com/100/thumb-1920-1004852.jpg'
        else:
            image = get['backdrop']
        
        # Set embed for profile (temp)
        emb = discord.Embed(
            title=get['name'],
            description=bio
        )
        emb.set_image(url=image)
        emb.set_thumbnail(url=avatar)
        return await ctx.send(embed=emb)
    
    @commands.command()
    async def bio(self, ctx, *, bio : str = None):
        if bio is None:
            return
        try:
            avatar_collection.update_one({'_id':ctx.author.id}, {'$set': {'bio': bio}})
        except:
            pass
        await ctx.send('aya')

    @commands.command()
    async def bg(self, ctx, *, backdrop : str = None):
        if backdrop is None:
            return
        try:
            avatar_collection.update_one({'_id':ctx.author.id}, {'$set': {'backdrop': backdrop}})
        except:
            pass
        await ctx.send('oyo')

def setup(bot):
    bot.add_cog(Tests(bot))

if __name__ == "__main__":
    db_client.test