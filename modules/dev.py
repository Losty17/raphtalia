import discord, os, ast, asyncio
from dotenv import load_dotenv
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont, ImageOps
from pymongo import MongoClient

load_dotenv()
OWNER = int(os.getenv('BOT_OWNER'))

##

db_client = MongoClient("mongodb+srv://Losty:%402Losty%40@raphtaliabot-nl6k6.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = db_client.get_database('guild_db')
collection = db.get_collection('guild_collection')
avatar_collection = db.get_collection('avatar_collection')

##

def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)

class DevOnly(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if ctx.author.id != OWNER:
            raise commands.NotOwner
        return ctx.author.id == OWNER

    @commands.command()
    async def teste(self, ctx):
        print('Tudo ok! u.u')
        await ctx.message.add_reaction('👌')

    @commands.command()
    async def emojis(self, ctx):
        await ctx.send(f'{ctx.guild.name}\'s emojis:\n')

        for emoji in ctx.guild.emojis:
            await ctx.send(f'{emoji.name} | {emoji.id}')

    @commands.command(hidden=True)
    async def load(self, ctx, *, module: str = None):
        if module is None:
            return await ctx.send('Módulo inválido')
        if not 'modules' in module:
            module = f'modules.{module}'
        try:
            self.bot.load_extension(module)
        except commands.ExtensionError as e:
            await ctx.send(f'{e.__class__.__name__}: {e}')
        else:
            await ctx.send(f'{module} foi carregado com sucesso')

    @commands.command(hidden=True)
    async def unload(self, ctx, *, module: str = None):
        if module is None:
            return await ctx.send('Módulo inválido')
        if not 'modules' in module:
            module = f'modules.{module}'
        try:
            self.bot.unload_extension(module)
        except commands.ExtensionError as e:
            await ctx.send(f'{e.__class__.__name__}: {e}')
        else:
            await ctx.send(f'{module} foi descarregado com sucesso')

    @commands.group(name='reload', hidden=True)
    async def reload(self, ctx, *, module: str = None):
        if module is None:
            return await ctx.send('Módulo inválido')
        if not 'modules' in module:
            module = f'modules.{module}'
        try:
            self.bot.reload_extension(module)
        except commands.ExtensionError as e:
            await ctx.send(f'{e.__class__.__name__}: {e}')
        else:
            await ctx.send(f'{module} foi recarregado com sucesso')

    @commands.command()
    async def eval(self, ctx, *, cmd):
        fn_name = "_eval_expr"

        cmd = cmd.strip("` ")

        # add a layer of indentation
        cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

        # wrap in async def body
        body = f"async def {fn_name}():\n{cmd}"

        parsed = ast.parse(body)
        body = parsed.body[0].body

        insert_returns(body)

        env = {
            'bot': ctx.bot,
            'discord': discord,
            'commands': commands,
            'ctx': ctx,
            '__import__': __import__
        }
        exec(compile(parsed, filename="<ast>", mode="exec"), env)

        result = (await eval(f"{fn_name}()", env))
        await ctx.send(result)

    @commands.command()
    async def chdata(self, ctx):
        await ctx.send('Channel data:')
        await ctx.send(ctx.channel.id)
        await ctx.send(ctx.channel.name)

    @commands.command()
    async def roledata(self, ctx):
        await ctx.send('Server roles:')
        for role in ctx.guild.roles:
            if role.name == '@everyone':
                continue
            await ctx.send(f'{role.name} | {role.id}')
        
    @commands.command()
    async def sleeptest(self, ctx):
        await ctx.send('teste')
        await asyncio.sleep(5)
        await ctx.send('teste2')
    
    @commands.command()
    async def hookdata(self, ctx):
        h = await ctx.channel.webhooks()
        whooks = []
        for wh in h:
            whooks.append(wh.name)
        print(whooks)
    
    @commands.command()
    async def teste3(self, ctx):
        muteRole = discord.utils.get(ctx.guild.roles, name="Roberto")
        if muteRole is not None:
            print(muteRole)
            print('Penis')

    @commands.command()
    async def mutetest(self, ctx):
        muteRole = discord.utils.get(ctx.guild.roles, name="Silenciado")
        
        if muteRole is not None:
            await ctx.author.add_roles(muteRole)
        else:
            await ctx.send('None')

    @commands.command()
    async def insertdb(self, ctx):
        try:
            collection.insert_one(
                {
                    '_id'    : ctx.guild.id,
                    'name'   : ctx.guild.name,
                    'prefix' : "r!",
                    'text'   : True,
                    'adm'    : True,
                    'images' : True,
                    'music'  : True,
                    'nsfw'   : True,
                    'welcome': False
                }
            )
        except:
            return await ctx.send('DOC já existe')
        await ctx.send(f'DB para `{ctx.guild.id} | {ctx.guild.name}` Criado com sucesso')

    @commands.command()
    async def getdb(self, ctx):
        return await ctx.send(f"`{collection.find_one({'_id': ctx.guild.id})}`")

    @commands.command()
    async def testdb(self, ctx):
        if collection.find_one({'_id': ctx.guild.id})['text'] == True:
            await ctx.send('pneis')

def setup(bot):
    bot.add_cog(DevOnly(bot))

if __name__ == "__main__":
    db_client.test