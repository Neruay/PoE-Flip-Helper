from data import gems
from utils import load_json, update_json, __DATA_PATH__
from prettytable import *
import requests
import json

def parse_gem_quality_data():
    alt_gems = {}
    for gem in gems:
        if gems[gem]["base_item"] != None and gems[gem]["base_item"]["display_name"].split(" ")[0] not in ["Vaal", "Awakened"] and gems[gem]["base_item"]["display_name"] not in alt_gems and len(gems[gem]["static"]["quality_stats"]) > 0:
            alt_gems[gems[gem]["base_item"]["display_name"]] = {"name": gems[gem]["base_item"]["display_name"], "qualities": {}}
            for quality in gems[gem]["static"]["quality_stats"]:
                match quality["set"]:
                    case item if item == 0: alt_gems[gems[gem]["base_item"]["display_name"]]["qualities"]["superior"] = {"type": "superior", "weight": quality["weight"], "price": 0}
                    case item if item == 1:  alt_gems[gems[gem]["base_item"]["display_name"]]["qualities"]["anomalous"] = {"type": "anomalous", "weight": quality["weight"], "price": 0}
                    case item if item == 2:  alt_gems[gems[gem]["base_item"]["display_name"]]["qualities"]["divergent"] = {"type": "divergent", "weight": quality["weight"], "price": 0}
                    case item if item == 3:  alt_gems[gems[gem]["base_item"]["display_name"]]["qualities"]["phantasmal"] = {"type": "phantasmal", "weight": quality["weight"], "price": 0}
    update_json(alt_gems, "alt_gems.json", __DATA_PATH__)

def get_gems_prices(alt_gems):
    for item in alt_gems:
        alt_gems[item]["qualities"]["superior"]["price"] = 1e7
        if "anomalous" in alt_gems[item]["qualities"]: alt_gems[item]["qualities"]["anomalous"]["price"] = 1e7
        if "divergent" in alt_gems[item]["qualities"]: alt_gems[item]["qualities"]["divergent"]["price"] = 1e7
        if "phantasmal" in alt_gems[item]["qualities"]: alt_gems[item]["qualities"]["phantasmal"]["price"] = 1e7
    ninja_url = "https://poe.ninja/api/data/itemoverview?league=Sanctum&type=SkillGem&language=en"
    response = json.loads(requests.get(ninja_url).content)
    number_of_entries = len(response["lines"])
    cnt = 1
    for item in response["lines"]:
        print("|{}/{}| Checking [{}] price, @poe.ninja".format(cnt, number_of_entries, item["name"]))
        cnt += 1
        gem_name = item["name"]
        if "Vaal" not in gem_name and "Awakened" not in gem_name and item["listingCount"] >= 2:
            if "corrupted" in item:
                if item["corrupted"] == True: continue
            match gem_name.split(" ")[0]:
                case "Anomalous":
                    if alt_gems[" ".join(gem_name.split(" ")[1:])]["qualities"]["anomalous"]["price"] > item["chaosValue"]:
                        alt_gems[" ".join(gem_name.split(" ")[1:])]["qualities"]["anomalous"]["price"] = item["chaosValue"]
                case "Divergent":
                    if alt_gems[" ".join(gem_name.split(" ")[1:])]["qualities"]["divergent"]["price"] > item["chaosValue"]:
                        alt_gems[" ".join(gem_name.split(" ")[1:])]["qualities"]["divergent"]["price"] = item["chaosValue"]
                case "Phantasmal":
                    if alt_gems[" ".join(gem_name.split(" ")[1:])]["qualities"]["phantasmal"]["price"] > item["chaosValue"]:
                        alt_gems[" ".join(gem_name.split(" ")[1:])]["qualities"]["phantasmal"]["price"] = item["chaosValue"]
                case _:
                    if alt_gems[gem_name]["qualities"]["superior"]["price"] > item["chaosValue"]:
                        alt_gems[gem_name]["qualities"]["superior"]["price"] = item["chaosValue"]
    for item in alt_gems:
        if alt_gems[item]["qualities"]["superior"]["price"] == 1e7: alt_gems[item]["qualities"]["superior"]["price"] = 1
        if "anomalous" in alt_gems[item]["qualities"] and alt_gems[item]["qualities"]["anomalous"]["price"] == 1e7: alt_gems[item]["qualities"]["anomalous"]["price"] = 1
        if "divergent" in alt_gems[item]["qualities"] and alt_gems[item]["qualities"]["divergent"]["price"] == 1e7: alt_gems[item]["qualities"]["divergent"]["price"] = 1
        if "phantasmal" in alt_gems[item]["qualities"] and alt_gems[item]["qualities"]["phantasmal"]["price"] == 1e7: alt_gems[item]["qualities"]["phantasmal"]["price"] = 1
    update_json(alt_gems, "alt_gems.json", __DATA_PATH__)

def find_gem_flips(alt_gems):
    profitable_flips = []
    currency = load_json("currency.json")
    active_lens_price = currency["Prime Regrading Lens"]["price"]
    support_lens_price = currency["Secondary Regrading Lens"]["price"]
    lens_type = None
    for gem in alt_gems:
        if "Support" in alt_gems[gem]["name"]: lens_type = support_lens_price
        else: lens_type = active_lens_price
        for current_quality in alt_gems[gem]["qualities"]:
            match current_quality:
                    case "superior": start = alt_gems[gem]["name"]
                    case "anomalous": start = "Anomalous " + alt_gems[gem]["name"]
                    case "divergent": start = "Divergent " + alt_gems[gem]["name"]
                    case "phantasmal": start = "Phantasmal " + alt_gems[gem]["name"]
            current_flip = ["{}\nPrice - {}".format(start, int(alt_gems[gem]["qualities"][current_quality]["price"]))]
            potential_profit = -(alt_gems[gem]["qualities"][current_quality]["price"] + lens_type)
            total_weight = 0
            for other_quality in alt_gems[gem]["qualities"]:
                if other_quality == current_quality: continue
                total_weight += alt_gems[gem]["qualities"][other_quality]["weight"]
            for other_quality in alt_gems[gem]["qualities"]:
                if other_quality == current_quality: continue
                match other_quality:
                    case "superior": target = alt_gems[gem]["name"]
                    case "anomalous": target = "Anomalous " + alt_gems[gem]["name"]
                    case "divergent": target = "Divergent " + alt_gems[gem]["name"]
                    case "phantasmal": target = "Phantasmal " + alt_gems[gem]["name"]
                current_value = alt_gems[gem]["qualities"][other_quality]["weight"] / total_weight * alt_gems[gem]["qualities"][other_quality]["price"]
                potential_profit += current_value
                current_flip.append("{}\nPrice - {}\n Chance to get - {}%".format(target, int(alt_gems[gem]["qualities"][other_quality]["price"]), round(alt_gems[gem]["qualities"][other_quality]["weight"] / total_weight * 100, 2)))
            while len(current_flip) < 4:
                current_flip.append("\n-")
            current_flip.append(round(potential_profit, 0))
            if potential_profit > 0:
                profitable_flips.append(current_flip)
    profitable_flips.sort(key=lambda i:i[4], reverse=True)
    return (profitable_flips)

def generate_flip_table(profitable_flips):
    flip_table = PrettyTable(hrules=ALL, padding_width=1)
    flip_table.set_style(SINGLE_BORDER)
    flip_table.field_names = ["START", "OUTCOME 1", "OUTCOME 2", "OUTCOME 3", "EXPECTED VALUE"]
    for flip in profitable_flips:
        flip_table.add_row(flip)
    print(flip_table)
#parse_gem_quality_data()
get_gems_prices(load_json("alt_gems.json", __DATA_PATH__))
generate_flip_table(find_gem_flips(load_json("alt_gems.json", __DATA_PATH__)))