import httpx
from datetime import datetime
from Class import Game

def get_free_epic_games():
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
                free_games.append(
                    Game(
                        title=game["title"],
                        store_link=f"https://www.epicgames.com/store/en-US/p/{game['productSlug']}"
                        if game["productSlug"]
                        else "https://www.epicgames.com/store/en-US/p/",
                        image_url=[
                            image["url"]
                            for image in game["keyImages"]
                            if image["type"] == "OfferImageWide"
                        ][0],
                    )
                )

    # print("## Free game(s)")
    # print(free_games)

    return free_games

# epic_free_games = get_free_epic_games()

# print(epic_free_games[0].store_link, epic_free_games[0].image_url)