import discord
import asyncio
import secret
from random import randint

client = discord.Client()
guild = discord.Guild

COR = 0xF26DDC 

TOKEN = secret.token()
msg_id = None
msg_user = None

@client.event
async def on_ready():
    print('OLA MUNDO!')
    await client.change_presence(activity = discord.Game('My prefix is "?" uwu'), status = discord.Status.idle)

@client.event
async def on_message(message):
    if message.content.lower().startswith('?help') or message.content.lower().startswith('?ajuda'):
        ajuda = discord.Embed(
            title = "Comandos: ",
            color = COR,
            description = "\n?help \n?teste \n?moeda"
        )
        await message.channel.send(embed = ajuda)

    if message.content.lower().startswith('?teste'):
        await message.channel.send('Hello world')

    if message.content.lower().startswith('?moeda'):
        if message.author.id == 207947146371006464:
            choice = randint(0,1)
            if choice == 0:
                await message.channel.send('Cara!')
                await message.add_reaction('😀')
            if choice == 1:
                await message.channel.send('Coroa!')
                await message.add_reaction('👑')
        else:
            await message.channel.send('Você não tem permissão para usar este comando!')

    if message.content.lower().startswith('?roles'):
        cargos = discord.Embed(
            title = "Selecione seus cargos!",
            color = COR,
            description = "» Programador - 👩‍💻\n» Artista - 👩‍🎨\n» Sonoplasta - 👩‍🎤",
        )
        botmsg = await message.channel.send(embed = cargos)
        await botmsg.add_reaction('👩‍💻')
        await botmsg.add_reaction('👩‍🎨')
        await botmsg.add_reaction('👩‍🎤')

        global msg_id
        msg_id = botmsg.id
        global msg_user
        msg_user = message.author

#### ?roles command, just works for https://discord.gg/dZMCKP7
@client.event
async def on_raw_reaction_add(payload):
    message_id = msg_id
    if message_id == msg_id:
        myRole = None
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

        if payload.emoji.name == '👩‍💻':
            myRole = discord.utils.get(guild.roles, name='💻dev')

        elif payload.emoji.name == '👩‍🎨':
            myRole = discord.utils.get(guild.roles, name='🎨artista')

        elif payload.emoji.name == '👩‍🎤':
            myRole = discord.utils.get(guild.roles, name='📢sonoplasta')

        if myRole != None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member != None:
                await member.add_roles(myRole)

@client.event
async def on_raw_reaction_remove(payload):
    message_id = msg_id
    if message_id == msg_id:
        myRole = None
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

        if payload.emoji.name == '👩‍💻':
            myRole = discord.utils.get(guild.roles, name='💻dev')

        elif payload.emoji.name == '👩‍🎨':
            myRole = discord.utils.get(guild.roles, name='🎨artista')

        elif payload.emoji.name == '👩‍🎤':
            myRole = discord.utils.get(guild.roles, name='📢sonoplasta')

        if myRole != None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member != 672901764747493397 and member != None:
                await member.remove_roles(myRole)
###

client.run(TOKEN)