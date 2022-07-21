from config import *
import os
from dotenv import load_dotenv
from games import *

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")


@bot.event
async def on_ready():
    
    guild_count = 0

    for guild in bot.guilds:
        print(f"(@) {guild.id} {guild.name}")
        # members = '\n - '.join([member.name for member in guild.members])
        # print(f"Guild Members in the Guild {guild.name} :\n - {members}")
        guild_count += 1

    print(f"StagBot running in {str(guild_count)} server(s).")

@bot.event 
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Hi {member.name}!\nWelcome to BuzzFeed Gaming!')

@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f"Unhandled message: {args[0]}\n")
        else: 
            raise


bot.run(DISCORD_TOKEN)