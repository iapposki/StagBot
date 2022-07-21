import math
import requests
import random
from config import *
import sys

async def get_random_reddit_meme(context, sub="dankmemes"):
    try :
        url = 'https://www.reddit.com/r/' + sub + '.json?sort=top&t=week'
        params = {'limit':100}
        resp = requests.get(url=url, params=params, headers={'User-agent': 'StagBot'}).json()
        rand_number = math.floor(random.random()*params['limit'])
        resp = resp["data"]["children"][rand_number]["data"]
        embedVar = discord.Embed(title=resp["title"], color=0x00ff00)
        embedVar.set_image(url=resp["url"])
        # embedVar.add_field(name="Field1", value="hi", inline=False)
        embedVar.set_footer(text="r/" + sub)
        await context.channel.send(embed=embedVar)
    except Exception as err:
        print("Error : ", sys.exc_info()[0], "occurred.")
        print(err)