import json
import discord
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

bot = discord.Client()

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
        print(f"- {guild.id} {guild.name}")
        guild_count += 1

    print(f"StagBot is in {str(guild_count)} server(s).")


@bot.event
async def on_message(message):
    if message.content == "hello":
        await message.channel.send("hey there!")


bot.run(DISCORD_TOKEN)