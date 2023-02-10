from utils import *
from utils import __CURRENT_PATH__
from price_info import *
import time

deli_orbs = load_json("deli_orbs.json")
essences = load_json("essences.json")
fossils = load_json("fossils.json")

item_types = ["fossils", "deli_orbs", "essences"]

for item_type in item_types:
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
        case _:
            pass

    for item in get_ninja_prices(ninja_query).items():
        if item_type == "essences" and item[0].split(" ")[0] not in ["Essence", "Deafening"]:
            continue
        if item[0] not in current_json:
            current_json[item[0]] = {"price": 0, "bulk_price": 0}
        current_json[item[0]]["price"] = item[1]

    quaries = generate_query(current_json.keys())
    poetrade_items = []
    proxy_list = load_json("proxy_list.json", __CURRENT_PATH__)
    cnt = 1
    proxy_cnt = 0
    for quary in quaries:
        print("|{}/{}| Checking {} bulk price at @pathofexile.com/trade".format(cnt, len(quaries), quary["query"]["type"]))
        poetrade_items.append(poetrade_query(quary, proxy=proxy_list[proxy_cnt]))
        time.sleep(2)
        cnt += 1
        if proxy_cnt == (len(proxy_list)-1): proxy_cnt = 0
        else: proxy_cnt += 1

    for item in poetrade_items:
        current_json[item[0]]["bulk_price"] = item[1]

    update_json(current_json, json_to_update)