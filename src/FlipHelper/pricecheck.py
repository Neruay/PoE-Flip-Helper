from utils import *
from price_info import *
import time

deli_orbs = load_json("deli_orbs.json")
essences = load_json("essences.json")

item_types = ["essences"]#, "deli_orbs"]

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
        case _:
            pass

    for item in get_ninja_prices(ninja_query).items():
        if item[0].split(" ")[0] not in ["Essence", "Deafening"]:
            continue
        if item[0] not in current_json:
            current_json[item[0]] = {"price": 0, "bulk_price": 0}
        current_json[item[0]]["price"] = item[1]

    quaries = generate_query(current_json.keys())
    poetrade_items = []
    cnt = 1
    for quary in quaries:
        print("Checking {}'s bulk price |{}/{}| Poetrade".format(quary["query"]["type"], cnt, len(quaries)))
        poetrade_items.append(poetrade_query(quary))
        time.sleep(10)
        cnt += 1

    for item in poetrade_items:
        current_json[item[0]]["bulk_price"] = item[1]

    update_json(current_json, json_to_update)