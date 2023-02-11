from utils import *
from utils import __CURRENT_PATH__
from price_info import *
from settings import BULK_SIZE
import time

deli_orbs = load_json("deli_orbs.json")
essences = load_json("essences.json")
fossils = load_json("fossils.json")
currency = load_json("currency.json")
oils = load_json("oils.json")
scarabs = load_json("scarabs.json")
catalysts = load_json("catalysts.json")

all_available_item_types = ["fossils", "deli_orbs", "essences", "oils", "currency", "scarabs", "catalysts"]
selected_item_type = "scarabs" #fossils, deli_orbs, essences, oils, currency, scarabs, catalysts, all

def update_prices(ninja_query: str, current_json, json_to_update):
    for item in get_ninja_prices(ninja_query).items():
        if ninja_query == "Essence" and item[0].split(" ")[0] not in ["Essence", "Deafening"]:
            continue
        if item[0] not in current_json and ninja_query == "Currency":
            current_json[item[0]] = {"price": 0, "in_divines": 0}
        if ninja_query == "Currency":
            in_divines = item[1] / current_json["Divine Orb"]["price"]
            if in_divines > 1.0: current_json[item[0]]["in_divines"] = round(item[1] / current_json["Divine Orb"]["price"], 1)
            elif in_divines > 0.1: current_json[item[0]]["in_divines"] = round(item[1] / current_json["Divine Orb"]["price"], 2)
            else: current_json[item[0]]["in_divines"] = round(item[1] / current_json["Divine Orb"]["price"], 3)
        if item[0] not in current_json: 
            current_json[item[0]] = {"price": 0, "bulk_price": 0}
        current_json[item[0]]["price"] = item[1]
    update_json(current_json, json_to_update)

def update_bulk_prices(current_json: dict, json_to_update, BULK_SIZE: int):
    quaries = generate_query(current_json.keys(), BULK_SIZE)
    poetrade_items = []
    proxy_list = load_json("proxy_list.json", __CURRENT_PATH__)
    cnt = 1
    proxy_cnt = 0 
    for quary in quaries:
        print("|{}/{}| Checking {} bulk price at @pathofexile.com/trade".format(cnt, len(quaries), quary["query"]["type"]))
        poetrade_items.append(poetrade_query(quary, proxy=proxy_list[proxy_cnt]))
        time.sleep(10)
        cnt += 1
        if proxy_cnt == (len(proxy_list)-1): proxy_cnt = 0
        else: proxy_cnt += 1
    for item in poetrade_items:
        if item[0] not in current_json:
            current_json[item[0]] = {"price": 0, "bulk_price": 0}
        current_json[item[0]]["bulk_price"] = item[1]
    update_json(current_json, json_to_update)

if selected_item_type == "all": types = all_available_item_types
else: types = [selected_item_type]
for item_type in types:
    json_to_update = ""
    current_json = ""
    ninja_query = ""
    match item_type:
        case "deli_orbs":
            json_to_update = "deli_orbs.json"
            current_json = deli_orbs
            ninja_query = "DeliriumOrb"
        case "essences":
            json_to_update = "essences.json"
            current_json = essences
            ninja_query = "Essence"
        case "fossils":
            json_to_update = "fossils.json"
            current_json = fossils
            ninja_query = "Fossil"
        case "currency":
            json_to_update = "currency.json"
            current_json = currency
            ninja_query = "Currency"
        case "oils":
            json_to_update = "oils.json"
            current_json = oils
            ninja_query = "Oil"
        case "scarabs":
            json_to_update = "scarabs.json"
            current_json = scarabs
            ninja_query = "Scarab"
        case "catalysts":
            json_to_update = "catalysts.json"
            current_json = catalysts
            ninja_query = "Currency"
        case _:
            assert current_json != "", "item_type error"

update_prices(ninja_query, current_json, json_to_update)
#update_bulk_prices(current_json, json_to_update, BULK_SIZE)

    

   