from config import *


async def get_random_reddit_meme(context, sub="dankmemes"):
    import requests
    import math
    import random
    import sys

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



"""Modified version of https://github.com/andrewguest/slack-free-epic-games"""
def get_free_epic_games():
    import httpx
    from datetime import datetime
    from classes import Game

    free_games_params = {
        "locale": "en-US",
        "country": "US",
        "allowCountries": "US",
    }

    # Epic's backend API URL for the free games promotion
    epic_api_url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions"

    # backend API request
    response = httpx.get(epic_api_url, params=free_games_params)
    
    # print("## HTTP response code")
    # print(response)
    # print("## HTTP response body")
    # print(response.json())

    # list of dictionaries containing information about the free games
    free_games = []

    # create Game objects for each entry found
    for game in response.json()["data"]["Catalog"]["searchStore"]["elements"]:
        if game["promotions"] and len(game["promotions"]["promotionalOffers"]) == 0:
            continue
        elif game["promotions"]:
            discount_price = game["price"]["totalPrice"]["discountPrice"]

            promo_start_date = datetime.strptime(game["promotions"]["promotionalOffers"][0]["promotionalOffers"][0]["startDate"],"%Y-%m-%dT%H:%M:%S.000%z",).replace(tzinfo=None)

            promo_end_date = datetime.strptime(game["promotions"]["promotionalOffers"][0]["promotionalOffers"][0]["endDate"],"%Y-%m-%dT%H:%M:%S.000%z",).replace(tzinfo=None)

            if (discount_price == 0 and promo_start_date <= datetime.now() <= promo_end_date):
                # print(game["keyImages"])
                try : 
                    free_games.append(
                        Game(
                            title=game["title"],
                            store_link=f"https://www.epicgames.com/store/en-US/p/{game['productSlug']}"
                            if game["productSlug"]
                            else "https://www.epicgames.com/store/en-US/free-games",
                            image_url=[
                                image["url"]
                                for image in game["keyImages"]
                                if image["type"] == "OfferImageWide"
                            ][0],
                        )
                    )
                except : 
                    print("An exception occured.")

    # print("## Free game(s)")
    # print(free_games)

    return free_games

def get_free_steam_games():
    from bs4 import BeautifulSoup
    import requests
    from classes import Game

    free_games = []
    STEAM_URL = "https://store.steampowered.com/search/?maxprice=free&specials=1"
    # STEAM_URL = "https://store.steampowered.com/search/?maxprice=free&tags=9%2C19%2C21%2C492%2C597%2C122%2C4182%2C599"
    request = requests.get(STEAM_URL)
    soup = BeautifulSoup(request.text, "html.parser")

    games = soup.find_all("a", class_="search_result_row")
    # print(soup)
    for game in games:
        game_name_class = game.find("span", class_="title")
        game_name = game_name_class.text
        # print(f"Game: {game_name}")

        game_url = game['href']
        # print(f"\tURL: {game_url}")

        game_id = game["data-ds-appid"]
        image_url = f"https://cdn.cloudflare.steamstatic.com/steam/apps/{game_id}/header.jpg"
        # print(f"\tImage: {image_url}")

        free_games.append(
            Game(
                title=game_name,
                store_link=game_url,
                image_url=image_url,
            )
        )
    return free_games