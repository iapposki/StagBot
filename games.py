from config import *


@bot.command(name="roll", help=" - Simulates dice roll. Args : [dice count] [dice side count]")
async def dice_roll(context, dice_count=1, dice_sides=6):
    import random
    resp = [str(random.choice(range(1, dice_sides + 1))) for _ in range(dice_count)]
    await context.send(" ".join(resp))
