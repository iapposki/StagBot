import discord
import os
from dotenv import load_dotenv
# from helperFunctions import *

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents().all()

bot = discord.Client(intents=intents)


# def guard_zero(func):
#     def inner(x,y):
#         if y == 0:
#             print("cannot divide by zero")
#             return 
#         return func(x,y)
#     return inner


# @guard_zero
# def divide(x,y) : 
#     return x/y

# print(divide(1,0))

@bot.event
async def on_ready():
    
    guild_count = 0

    for guild in bot.guilds:
        print(f"(@) {guild.id} {guild.name}")
        members = '\n - '.join([member.name for member in guild.members])
        print(f"Guild Members in the Guild {guild.name} :\n - {members}")
        guild_count += 1

    print(f"StagBot is in {str(guild_count)} server(s).")

@bot.event
async def on_member_join(member):
    await member.create_dm()

@bot.event
async def on_message(message):
    try:
        if message.content[0] == "~":
            commands = message.content.split(" ")
            # print(commands)
            # if commands[0] == "~get":
            await message.channel.send("command recognized")
    except:
        pass

@bot.event 
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Hi {member.name}!\nWelcome to BuzzFeed Gaming!')


bot.run(DISCORD_TOKEN)