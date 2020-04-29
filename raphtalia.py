# # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                 #
#   ______            _     _        _ _          #
#   | ___ \          | |   | |      | (_)         #
#   | |_/ /__ _ _ __ | |__ | |_ __ _| |_  __ _    #
#   |    // _` | '_ \| '_ \| __/ _` | | |/ _` |   #
#   | |\ \ (_| | |_) | | | | || (_| | | | (_| |   #
#   \_| \_\__,_| .__/|_| |_|\__\__,_|_|_|\__,_|   #
#              | |                                #
#              |_|                                #
#                                                 #
#       Copyright © 2020 raphtalia.kody.mobi      #
#               All rights reserved.              #
#                                                 #
# # # # # # # # # # # # # # # # # # # # # # # # # #
import discord
from discord.ext import commands
from os import getenv
from dotenv import load_dotenv
from pymongo import MongoClient
from sys import exit
try:
    from modules import *
except ImportError as error:
    exit(f'ERROR: Missing dependency: {error}')

# Get bot token
load_dotenv()
TOKEN = getenv('BOT_TOKEN')

# List of extensions to load
extensions = [
    'modules.core',
    'modules.adm',
    'modules.text',
    'modules.images',
    'modules.nsfw',
    'modules.music',
    'modules.dev',
    'modules.error_handler',
    'modules.tests'
]

# Database connection
db_client = MongoClient("mongodb+srv://Losty:%402Losty%40@raphtaliabot-nl6k6.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = db_client.get_database('guild_db')
collection = db.get_collection('guild_collection')

# Custom prefix def
default_prefix = '.'
async def determine_prefix(bot, message):
    guild = message.guild
    if guild:
        prefix = collection.find_one({'_id': guild.id})['prefix']
        return prefix
    else: return default_prefix

# Bot creation
bot = commands.Bot(command_prefix=determine_prefix,help_command=None,case_insensitive=True,owner_id=int(getenv('BOT_OWNER')))      

# Function for loading all modules
def load_modules():
    for e in extensions:
        try:
            print(f"Carregando módulo: {e}...")
            bot.load_extension(e)
        except Exception:
            print(f"Não foi possível carregar o módulo {e}")

# Letta run the boat
if __name__ == "__main__":
    load_modules()
    try:
        bot.run(TOKEN)
    except KeyError:
        print('Váriavel de ambiente não encontrada.')
    