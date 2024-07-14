import discord
from discord.ext import commands

from Afkmove import Afkmove

intents = discord.Intents.all()
client = commands.Bot(command_prefix='sb!', intents=intents)   

GUILD_ID = YOUR_GUILD ID
TARGET_CHANNEL_ID = YOUR_VOICE_TARGET  
VOICE_CHANNEL_IDS = [ 
    YOUR VOICE CHANNEL,
    YOUR VOICE CHANNEL # you can add more voice channel id
]

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    print(f'Bot is connected to guilds :')
    for guild in client.guilds:
        print(f'- {guild.name} (ID: {guild.id})')

    afk_move = Afkmove(client, GUILD_ID, TARGET_CHANNEL_ID, VOICE_CHANNEL_IDS)
    afk_move.register_events()
    afk_move.check_muted_users.start()

client.run("YOUR_TOKEN")   
