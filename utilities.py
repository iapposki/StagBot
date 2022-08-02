from config import *
import sys

@bot.command(name="free-games", help=" - Gets currently free games to grab (supports only epic games and steam games for now)")
async def get_free_games(context):
    from libraries import get_free_epic_games, get_free_steam_games
    data = get_free_epic_games()
    data += get_free_steam_games()
<<<<<<< HEAD
    data = []
=======
>>>>>>> 5927adc203f26001f0fd8d7d6787ca7613a29f06
    if len(data) == 0:
        await context.channel.send("No free games for now!")
    else:
        for i in range(len(data)):
            try:
                url = data[i].store_link
                img_url = data[i].image_url
                embedVar = discord.Embed(title=data[i].title, url=url, color=0x00ff00)
                embedVar.set_image(url=img_url)
                await context.channel.send(embed=embedVar)
            except Exception as err:
                print("Error : ", sys.exc_info()[0], "occurred.")
<<<<<<< HEAD
                print(err)
=======
                print(err)
>>>>>>> 5927adc203f26001f0fd8d7d6787ca7613a29f06
