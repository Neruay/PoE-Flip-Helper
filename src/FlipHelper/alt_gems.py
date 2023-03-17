from data import gems
from utils import load_json, update_json, __DATA_PATH__
from prettytable import *
import requests
import json
import argparse

def parse_gem_quality_data() -> None:
    alt_gems = {}
    for gem in gems:
        if gems[gem]["base_item"] != None and gems[gem]["base_item"]["display_name"].split(" ")[0] not in ["Vaal", "Awakened"] and gems[gem]["base_item"]["display_name"] not in alt_gems and len(gems[gem]["static"]["quality_stats"]) > 0:
            alt_gems[gems[gem]["base_item"]["display_name"]] = {"name": gems[gem]["base_item"]["display_name"], "qualities": {}, "qualities21": {}}
            for quality in gems[gem]["static"]["quality_stats"]:
                match quality["set"]:
                    case item if item == 0: 
                        alt_gems[gems[gem]["base_item"]["display_name"]]["qualities"]["superior"] = {"type": "superior", "weight": quality["weight"], "price": 0}
                        alt_gems[gems[gem]["base_item"]["display_name"]]["qualities21"]["superior"] = {"type": "superior", "weight": quality["weight"], "price": 0, "listed": 0}
                    case item if item == 1:  
                        alt_gems[gems[gem]["base_item"]["display_name"]]["qualities"]["anomalous"] = {"type": "anomalous", "weight": quality["weight"], "price": 0}
                        alt_gems[gems[gem]["base_item"]["display_name"]]["qualities21"]["anomalous"] = {"type": "anomalous", "weight": quality["weight"], "price": 0, "listed": 0}
                    case item if item == 2:  
                        alt_gems[gems[gem]["base_item"]["display_name"]]["qualities"]["divergent"] = {"type": "divergent", "weight": quality["weight"], "price": 0}
                        alt_gems[gems[gem]["base_item"]["display_name"]]["qualities21"]["divergent"] = {"type": "divergent", "weight": quality["weight"], "price": 0, "listed": 0}
                    case item if item == 3:  
                        alt_gems[gems[gem]["base_item"]["display_name"]]["qualities"]["phantasmal"] = {"type": "phantasmal", "weight": quality["weight"], "price": 0}
                        alt_gems[gems[gem]["base_item"]["display_name"]]["qualities21"]["phantasmal"] = {"type": "phantasmal", "weight": quality["weight"], "price": 0, "listed": 0}
    update_json(alt_gems, "alt_gems.json", __DATA_PATH__)

def get_gems_prices(alt_gems: dict) -> None:
    for item in alt_gems:
        alt_gems[item]["qualities"]["superior"]["price"] = 1e7
        alt_gems[item]["qualities21"]["superior"]["price"] = 1e7
        if "anomalous" in alt_gems[item]["qualities"]: 
            alt_gems[item]["qualities"]["anomalous"]["price"] = 1e7
            alt_gems[item]["qualities21"]["anomalous"]["price"] = 1e7
        if "divergent" in alt_gems[item]["qualities"]: 
            alt_gems[item]["qualities"]["divergent"]["price"] = 1e7
            alt_gems[item]["qualities21"]["divergent"]["price"] = 1e7
        if "phantasmal" in alt_gems[item]["qualities"]: 
            alt_gems[item]["qualities"]["phantasmal"]["price"] = 1e7
            alt_gems[item]["qualities21"]["phantasmal"]["price"] = 1e7
    ninja_url = "https://poe.ninja/api/data/itemoverview?league=Sanctum&type=SkillGem&language=en"
    response = json.loads(requests.get(ninja_url).content)
    number_of_entries = len(response["lines"])
    cnt = 1
    for item in response["lines"]:
        print("|{}/{}| Checking [{}] price, @poe.ninja".format(cnt, number_of_entries, item["name"]))
        cnt += 1
        gem_name = item["name"]
        if "Vaal" not in gem_name and "Awakened" not in gem_name and item["listingCount"] >= 3:
            if "corrupted" not in item:
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
        if "Vaal" not in gem_name and "Awakened" not in gem_name and item["listingCount"] >= 3:
            if item["variant"] != "21/20c": continue
            match gem_name.split(" ")[0]:
                case "Anomalous":
                    if alt_gems[" ".join(gem_name.split(" ")[1:])]["qualities21"]["anomalous"]["price"] > item["chaosValue"]:
                        alt_gems[" ".join(gem_name.split(" ")[1:])]["qualities21"]["anomalous"]["price"] = item["chaosValue"]
                        alt_gems[" ".join(gem_name.split(" ")[1:])]["qualities21"]["anomalous"]["listed"] = item["listingCount"]
                case "Divergent":
                    if alt_gems[" ".join(gem_name.split(" ")[1:])]["qualities21"]["divergent"]["price"] > item["chaosValue"]:
                        alt_gems[" ".join(gem_name.split(" ")[1:])]["qualities21"]["divergent"]["price"] = item["chaosValue"]
                        alt_gems[" ".join(gem_name.split(" ")[1:])]["qualities21"]["divergent"]["listed"] = item["listingCount"]
                case "Phantasmal":
                    if alt_gems[" ".join(gem_name.split(" ")[1:])]["qualities21"]["phantasmal"]["price"] > item["chaosValue"]:
                        alt_gems[" ".join(gem_name.split(" ")[1:])]["qualities21"]["phantasmal"]["price"] = item["chaosValue"]
                        alt_gems[" ".join(gem_name.split(" ")[1:])]["qualities21"]["phantasmal"]["listed"] = item["listingCount"]
                case _:
                    if alt_gems[gem_name]["qualities21"]["superior"]["price"] > item["chaosValue"]:
                        alt_gems[gem_name]["qualities21"]["superior"]["price"] = item["chaosValue"]   
                        alt_gems[gem_name]["qualities21"]["superior"]["listed"] = item["listingCount"]
    for item in alt_gems:
        if alt_gems[item]["qualities"]["superior"]["price"] == 1e7: alt_gems[item]["qualities"]["superior"]["price"] = 1
        if "anomalous" in alt_gems[item]["qualities"] and alt_gems[item]["qualities"]["anomalous"]["price"] == 1e7: alt_gems[item]["qualities"]["anomalous"]["price"] = 1
        if "divergent" in alt_gems[item]["qualities"] and alt_gems[item]["qualities"]["divergent"]["price"] == 1e7: alt_gems[item]["qualities"]["divergent"]["price"] = 1
        if "phantasmal" in alt_gems[item]["qualities"] and alt_gems[item]["qualities"]["phantasmal"]["price"] == 1e7: alt_gems[item]["qualities"]["phantasmal"]["price"] = 1
        if alt_gems[item]["qualities21"]["superior"]["price"] == 1e7: alt_gems[item]["qualities21"]["superior"]["price"] = 1
        if "anomalous" in alt_gems[item]["qualities21"] and alt_gems[item]["qualities21"]["anomalous"]["price"] == 1e7: alt_gems[item]["qualities21"]["anomalous"]["price"] = 1
        if "divergent" in alt_gems[item]["qualities21"] and alt_gems[item]["qualities21"]["divergent"]["price"] == 1e7: alt_gems[item]["qualities21"]["divergent"]["price"] = 1
        if "phantasmal" in alt_gems[item]["qualities21"] and alt_gems[item]["qualities21"]["phantasmal"]["price"] == 1e7: alt_gems[item]["qualities21"]["phantasmal"]["price"] = 1
    update_json(alt_gems, "alt_gems.json", __DATA_PATH__)

def find_gem_flips(alt_gems: dict) -> list:
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
            expected_profit = -(alt_gems[gem]["qualities"][current_quality]["price"] + lens_type)
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
                expected_profit += current_value
                current_flip.append("{}\nPrice - {}\n Chance to get - {}%".format(target, int(alt_gems[gem]["qualities"][other_quality]["price"]), round(alt_gems[gem]["qualities"][other_quality]["weight"] / total_weight * 100, 2)))
            while len(current_flip) < 4:
                current_flip.append("\n-")
            current_flip.append(round(expected_profit, 0))
            if expected_profit > 0:
                profitable_flips.append(current_flip)
    profitable_flips.sort(key=lambda i:i[4], reverse=True)
    return (profitable_flips)

def generate_flip_table(profitable_flips: list) -> None:
    flip_table = PrettyTable(hrules=ALL, padding_width=1)
    flip_table.set_style(SINGLE_BORDER)
    flip_table.field_names = ["START", "OUTCOME 1", "OUTCOME 2", "OUTCOME 3", "EXPECTED VALUE"]
    for flip in profitable_flips:
        flip_table.add_row(flip)
    print(flip_table)

def find_gems_for_leveling(alt_gems: dict) -> list:
    price_differences = []
    for gem in alt_gems:
        for quality in alt_gems[gem]["qualities"]:
            match quality:
                case "superior": current_gem = alt_gems[gem]["name"]
                case "anomalous": current_gem = "Anomalous " + alt_gems[gem]["name"]
                case "divergent": current_gem = "Divergent " + alt_gems[gem]["name"]
                case "phantasmal": current_gem = "Phantasmal " + alt_gems[gem]["name"]
            base_price = int(alt_gems[gem]["qualities"][quality]["price"])
            final_price = int(alt_gems[gem]["qualities21"][quality]["price"])
            price_diff = int(alt_gems[gem]["qualities21"][quality]["price"] - alt_gems[gem]["qualities"][quality]["price"])
            listed = alt_gems[gem]["qualities21"][quality]["listed"]
            current_diff = [current_gem, base_price, final_price, price_diff, listed]
            price_differences.append(current_diff)
    return price_differences

def generate_gems_leveling_table(price_differences: list) -> None:
    level_table = PrettyTable(hrules=ALL, padding_width=1)
    level_table.set_style(SINGLE_BORDER)
    level_table.field_names = ["GEM", "BASE PRICE", "21/20 PRICE", "DIFFERENCE", "LISTED ON MARKET"]
    for diff in price_differences:
        level_table.add_row(diff)
    print(level_table.get_string(sortby="DIFFERENCE", reversesort=True, end=20))

def run(*args) -> None:
    match args[0]:
        case "parse_gems": parse_gem_quality_data()
        case "get_gems_prices": get_gems_prices(load_json("alt_gems.json", __DATA_PATH__))
        case "generate_flip_table": generate_flip_table(find_gem_flips(load_json("alt_gems.json", __DATA_PATH__)))
        case "generate_gems_leveling_table": generate_gems_leveling_table(find_gems_for_leveling(load_json("alt_gems.json", __DATA_PATH__)))

if __name__ == "__main__":
    import sys
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "mode",
    )
    parser.add_argument(
        "item_type",
        nargs="?",
        default=0
    )
    args = parser.parse_args()
    arg_list = [args.mode, args.item_type] if args.item_type else [args.mode]
    sys.exit(run(*arg_list))