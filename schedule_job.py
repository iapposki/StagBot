import aiohttp
from config import *
import numpy as np
from libraries import get_free_epic_games, get_free_steam_games
import sys

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

class Scheduler(commands.Cog):
    """Schedule commands."""
    def __init__(self, bot):
        self.bot = bot

        # Initialize session
        self.session = aiohttp.ClientSession()
    
    # Scheduled events
    async def schedule_func(self):
        data = get_free_epic_games()
        data += get_free_steam_games()
        array = np.load('fglist.npy')
        # print('running')
        for element in data:
            if element.title not in array[-10:]:    
                array = np.append(array,[element.title])
                url = element.store_link
                img_url = element.image_url
                embedVar = discord.Embed(title=element.title, url=url, color=0x00ff00)
                embedVar.set_image(url=img_url)
                for guild in bot.guilds:
                    try:
                        
                        await guild.text_channels[0].send(embed = embedVar)
                        # await context.channel.send(embed=embedVar)
                    except Exception as err:
                        print("Error : ", sys.exc_info()[0], "occurred.")
                        print(err)
                    
                # print(element.title)
        np.save('fglist.npy', array)

    def schedule(self):
        # Initialize scheduler
        # job_defaults = {
        #     "coalesce": True,
        #     "max_instances": 5,
        #     "misfire_grace_time": 15,
        #     "replace_existing": True,
        # }

        # scheduler = AsyncIOScheduler(job_defaults = job_defaults)
        scheduler = AsyncIOScheduler()


        # Add jobs to scheduler
        scheduler.add_job(self.schedule_func, CronTrigger.from_crontab("0 * * * *"),misfire_grace_time=300) 
        # Every hour
        return scheduler