import discord
import time

from discord.ext import commands
from random import choice
from random import randint

def is_empty(anything):
    if anything:
        return False
    else:
        return True

COR = 0xF26DDC

class Text(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
    async def diga(self, ctx, *args):
        if is_empty(args):
            await ctx.message.channel.send(f'{ctx.author.mention} o que eu deveria dizer? -.-')
        else:
            mesg = ' '.join(args)
            if mesg.lower() == 'pindamonhangaba':
                await ctx.message.channel.send('Achou que eu ia falar? bobinho')
            else:
                await ctx.message.delete()
                await ctx.message.channel.send(mesg)

    @commands.command(aliases=['invert'])
    async def inverter(self, ctx, *, text: str = None):
        if text is not None:
            to_reverse = text
            await ctx.channel.send(str(to_reverse)[::-1])
        else:
            return

    @commands.command(aliases=['choice'])
    async def escolha(self, ctx, *args):
        if is_empty(args):
            await ctx.channel.send(f'{ctx.author.mention} Quais eram as opções mesmo? ;-;')
        else:
            await ctx.channel.send(choice(args))

    @commands.command(aliases=['add'])
    async def some(self, ctx, left: int, right: int):
        try:
            await ctx.send(left + right)
        except:
            await ctx.send('Não consegui efetuar, tente novamente')

    @commands.command(aliases=['roll','dice','rolldice'])
    async def role(self, ctx, *args):
        if is_empty(args):
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
                    time.sleep(2)
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

def setup(bot):
    bot.add_cog(Text(bot))

if __name__ == "__main__":
    pass