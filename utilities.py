from config import *
import sys
import asyncio
import pickle

@bot.command(name="free-games", help=" - Gets currently free games to grab (supports only epic games and steam games for now)")
async def get_free_games(context):
    from libraries import get_free_epic_games, get_free_steam_games
    data = get_free_epic_games()
    data += get_free_steam_games()
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
                print(err)

@bot.command(name="setup-ticket-system", help=" - Sets up the ticketing system.")
async def setup_ticket_system(context):
    from libraries import get_categories_list
    await context.channel.send("Enter the serial id (from below) for the category you would like to make temporary channels for tickets in : ")
    category_list = get_categories_list(context)
    response = []
    i = 1
    for category in category_list:
        response.append("(" + str(i) + ") " + str(category) + " \n")

        i += 1

    response.append(f"({str(i)}) Default(Tickets) \n")
    await context.channel.send("".join(response))
    
    def check_category(msg):
        return 0 < int(msg.content) < len(response) + 1
    try:
        msg = await bot.wait_for("message", check=check_category, timeout=30.0)
    except asyncio.TimeoutError:
        await context.send(f"**{context.author}**, you didn't send a valid response in the last 30 seconds in this channel, please restart the process. ")
        return
    else:
        await context.send("You have selected the category : " + str(response[int(msg.content)-1]))
        if int(msg.content) == len(response):
            category = discord.utils.get(context.guild.categories, name="Tickets")
            if category is None:
                category = await context.guild.create_category("Tickets")
        else: 
            category = discord.utils.get(context.guild.categories, name=str(category_list[int(msg.content)-1]))
            print(category_list[int(msg.content)-1], category)
        
        with open('./guild_preferences.txt', 'rb') as file:
            data = pickle.Unpickler(file)
            data = data.load() 
            # print(data)
        with open('./guild_preferences.txt', 'wb') as file:
            data[str(context.message.guild.id)] = {'ticket_default_channel' : category.name}
            # print(data)
            try:
                pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)
            except Exception as e:
                print(Exception)
        with open('./guild_preferences.txt', 'rb') as file:
            data = pickle.Unpickler(file)
            data = data.load()
            # print(data)
        # print(context.message.guild.id)

@bot.command(name="create-ticket", help=" - Creates tickets only visible to the user creating it and the user with role 'admin'.")
async def create_ticket(context):
    with open('./guild_preferences.txt', 'rb') as file:
        data = pickle.Unpickler(file)
        data = data.load()
        # print(data)
    if not data[str(context.message.guild.id)] or not data[str(context.message.guild.id)]['ticket_default_channel']:
        category = discord.utils.get(context.guild.categories, name="Tickets")
        if category is None:
            category = await context.guild.create_category("Tickets")
        data[str(context.message.guild.id)] = {'ticket_default_channel' : category.name}
        with open('./guild_preferences.txt', 'wb') as file:
            try:
                pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)
            except Exception as e:
                print(e)

    category_name = data[str(context.message.guild.id)]['ticket_default_channel']
    category = discord.utils.get(context.guild.categories, name=str(category_name))
    channel = discord.utils.get(context.guild.text_channels, name=f"ticket-{(context.author.name).lower()}-{context.author.discriminator}", category=category)
    if channel is None:
        channel = await context.guild.create_text_channel(f"ticket-{(context.author.name).lower()}-{context.author.discriminator}", category=category)
    # add the user and admin to the channel
    everyone_role = context.guild.default_role
    everyone_permissions = discord.PermissionOverwrite(read_messages=False, send_messages=False)
    await channel.set_permissions(everyone_role, overwrite=everyone_permissions)
    await channel.set_permissions(context.author, read_messages=True, send_messages=True)
    for role in context.guild.roles:
        if role.name == "admin":
            await channel.set_permissions(role, read_messages=True, send_messages=True)
    await context.channel.send(f"Ticket created in {channel.mention}")
    


# @bot.command(name="chain")
# async def greet(context):
#     await context.send("Say hello!")

#     def check(m):
#         return m.content == "hello" and m.channel == context.channel
#     with open('./guild_preferences.txt', 'wb') as file:
#         # data = pickle.load(file)
#         guild_preferences = {"424404218170966016" : {}}
#         pickle.dump(guild_preferences, file, protocol=pickle.HIGHEST_PROTOCOL)
#         print('ok')

#     msg = await bot.wait_for("message", check=check)
#     # msg = await bot.wait_for('m')
#     await context.send(f"Hello {msg.author}!")