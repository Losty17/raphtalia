import discord, time, os, asyncio
from discord.ext import commands
from random import choice, randint
from pymongo import MongoClient

class Text(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.words_file = open(os.path.join('media', 'words.txt'), "r")
        self.words = self.words_file.readlines()

        self.words_file.close()

        self.db_client = MongoClient("mongodb+srv://Losty:%402Losty%40@raphtaliabot-nl6k6.gcp.mongodb.net/test?retryWrites=true&w=majority")
        self.db = self.db_client.get_database('guild_db')
        self.collection = self.db.get_collection('guild_collection')
    
    async def cog_check(self, ctx):
        if ctx.guild: return True
        col = self.collection.find_one({'_id': ctx.guild.id})
        if col['text'] == False:
            raise commands.DisabledCommand
        return col['text'] == True

    @commands.command(pass_context=True)
    async def ping(self, ctx):
        mesgedit = await ctx.channel.send('Ping?')
        before = time.monotonic()
        await mesgedit.edit(content=f"{ctx.author.mention} Pong!")
        ping = (time.monotonic() - before) * 1000
        await mesgedit.edit(content=f"{ctx.author.mention} Pong!  Minha latência é de `{int(ping)}ms`, a latência da API é de `{int(self.bot.latency * 1000)}ms`")

    @commands.command(aliases=['flip', 'coin', 'flipcoin'])
    async def moeda(self, message):
        coin = ['Cara!', 'Coroa!']
        pau = choice(coin)
        await message.channel.send(f'{message.author.mention} {pau}')

    @commands.command(pass_context = True, aliases=['say'])
    async def diga(self, ctx, *, args : str = None):
        if args == None: return
        if args.lower() == 'pindamonhangaba':
            await ctx.channel.send('Achou que eu ia falar? bobinho')
        else:
            await ctx.message.delete()
            return await ctx.channel.send(args)

    @commands.command(aliases=['invert'])
    async def inverter(self, ctx, *, text: str = None):
        if text is not None:
            to_reverse = text
            await ctx.channel.send(str(to_reverse)[::-1])
        else:
            return

    @commands.command(aliases=['choice', 'chose', 'pick', 'choose'])
    async def escolha(self, ctx, *args):
        if args:
            await ctx.channel.send(choice(args))
        else:
            await ctx.channel.send(f'{ctx.author.mention} Quais eram as opções mesmo? ;-;')

    @commands.command(aliases=['add'])
    async def some(self, ctx, left: int, right: int):
        try:
            await ctx.send(left + right)
        except:
            await ctx.send('Não consegui efetuar, tente novamente')

    @commands.command(aliases=['roll','dice','rolldice'])
    async def role(self, ctx, *args):
        if not args:
            return await ctx.send('Qual deveria ser o número para rolar?')
        roll = ''.join(args)
        
        async with ctx.typing():
            if 'd' in roll:
                try:
                    dice, faces = roll.split('d')
                    nums_str = []
                    nums_int = []
                    for i in range(int(dice)):
                        result = randint(1, int(faces))
                        nums_int.append(result)
                        nums_str.append(str(result))
                    final_result = sum(nums_int)
                    partial = ' + '.join(nums_str)
                    await ctx.send('Rolando...')
                    await asyncio.sleep(1)
                    await ctx.send(f'{ctx.author.mention}, `{partial}` = `{str(final_result)}` 🎲')
                except:
                    await ctx.send('Não consegui efetuar a operação, tente novamente')
            else:
                try:
                    await ctx.send('Rolando...')
                    time.sleep(2)
                    dice = randint(1, int(roll))
                    await ctx.send(f'{ctx.author.mention}, `{dice}` 🎲')
                except:
                    await ctx.send('Não consegui efetuar a operação, tente novamente')
    
    @commands.command(aliases=['autor'])
    async def author(self, ctx):
        await ctx.send('Siga meu criador nas redes sociais!\n- https://twitter.com/KKKBini\n- https://discord.gg/df7XWzt\n- https://anilist.co/user/losty17')

    @commands.command()
    async def lal(self, ctx):
        await ctx.send('LAL')

    @commands.command(pass_context=True,aliases=['8ball'])
    async def filo(self, ctx, question : str = None):
        if not question: return
        else: 
            ans = [
                'Sim',
                'Não',
                'Talvez',
                'Não sei',
                'Concordo',
                'Com certeza',
                'Obviamente não',
                'Não posso negar',
                'Não posso afirmar',
                '(Censurado pelo governo)',
                'Com toda certeza que sim',
                'Para de encher o saco e vai capinar um lote, não tô aqui pra te responder'
            ]
            msg = choice(ans)
        
        # Finding the webhook
        filo = discord.utils.get(await ctx.channel.webhooks(), name='Filo-chan')
        if not filo:
            with open(os.path.join("media", "filo.png"), 'rb') as avatar:
                filo = await ctx.channel.create_webhook(name='Filo-chan',avatar=avatar.read())
        
        # Sending the message
        return await filo.send(content=msg)

    @commands.command()
    async def proibir(self, ctx, *, proibicao : str = None):
        # Setting the prohibition
        if proibicao: msg = f'Hoje o governo proibiu {proibicao}'
        else: msg = f'Hoje o governo proibiu {choice(self.words).lower()}'
        
        # Finding the webhook
        proibiubot = discord.utils.get(await ctx.channel.webhooks(), name='ProibiuBOT')
        if not proibiubot:
            with open(os.path.join("media", "proibiu.jpg"), 'rb') as avatar:
                proibiubot = await ctx.channel.create_webhook(name='ProibiuBOT',avatar=avatar.read())
        
        # Sending the message
        return await proibiubot.send(content=msg)

def setup(bot):
    bot.add_cog(Text(bot))

if __name__ == "__main__":
    pass