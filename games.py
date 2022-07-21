from config import *


@bot.command(name="roll", help=" - Simulates dice roll. Optional Args : [dice count] [dice side count]")
async def dice_roll(context, dice_count=1, dice_sides=6):
    import random
    resp = [str(random.choice(range(1, dice_sides + 1))) for _ in range(dice_count)]
    await context.send(" ".join(resp))

@bot.command(name="meme", help=" - Gets a random meme from reddit's r/dankmeme (default) weekly top 100. Optional Arg: [subreddit]")
async def get_meme(context, sub = "dankmemes"):
    from libraries import get_random_reddit_meme
    await get_random_reddit_meme(context, sub)