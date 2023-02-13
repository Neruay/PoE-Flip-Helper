from price_info import *
from utils import *
from settings import BULK_SIZE
from prettytable import *

deli_orbs = load_json("deli_orbs.json")
essences = load_json("essences.json")
fossils = load_json("fossils.json")
currency = load_json("currency.json")
oils = load_json("oils.json")
scarabs = load_json("scarabs.json")
catalysts = load_json("catalysts.json")

scarabs_winged = {}
scarabs_gilded = {}
for item in scarabs:
    if item.split()[0] == "Winged": scarabs_winged[item] = scarabs[item]
    else: scarabs_gilded[item] = scarabs[item]

all_available_item_types = [(fossils, "Fossils"), (deli_orbs, "Deli Orbs"), (essences, "Essences"), (scarabs_gilded, "Gilded Scarabs"), (scarabs_winged, "Winged Scarabs"), (catalysts, "Catalysts")] #(oils, "Oils"), (catalysts, "Catalysts")]
yellow_juice_price = currency["Vivid Crystallised Lifeforce"]["price"]
blue_juice_price = currency["Primal Crystallised Lifeforce"]["price"]
purple_juice_price = currency["Wild Crystallised Lifeforce"]["price"]

divine_price = currency["Divine Orb"]["price"]

stack_change_prices = {
    "roll_deli_orbs": blue_juice_price * 30,
    "roll_essences": blue_juice_price * 30,
    "roll_fossils": purple_juice_price * 30,
    "roll_oils": yellow_juice_price * 30,
    "roll_scarabs": purple_juice_price * 30,
    "roll_catalysts": yellow_juice_price * 30
}

def get_keep_list(item_type):
    keep_list = []
    match item_type:
        case item if item == deli_orbs: current_json = "deli_orbs.json"
        case item if item == essences: current_json = "essences.json"
        case item if item == fossils: current_json = "fossils.json"
        case item if item == oils: current_json = "oils.json"
        case item if item == scarabs_gilded or item == scarabs_winged: current_json = "scarabs.json"
        case item if item == catalysts: current_json == "catalysts.json"
        case _: print("Item-type error")
    item_info = load_json(current_json)
    for item in item_info:
        if item_info[item]["roll_keep"] == True:
            keep_list.append(item)
    return keep_list

def calculate_average_profit(item_type):
    outcomes = []
    roll_item_prices = []
    avg_roll_item_price = 0
    success_rate = 0
    average_profit_per_roll = 0
    for item in item_type:
        if item_type[item]["roll_keep"] == True:
            success_rate += item_type[item]["weight"]
            outcomes.append([item_type[item]["bulk_price"], item_type[item]["weight"]])
        else: roll_item_prices.append(item_type[item]["price"])
    if len(roll_item_prices) > 0: avg_roll_item_price = round(sum(roll_item_prices)/len(roll_item_prices), 2)
    if success_rate > 0:
        average_rolls_to_hit = round(1/success_rate, 3)
    else: return -1
    for outcome in outcomes:
        average_profit_per_roll += (outcome[0] * outcome[1] * average_rolls_to_hit)
    match item_type:
        case item if item == deli_orbs: roll_cost = stack_change_prices["roll_deli_orbs"]
        case item if item == essences: roll_cost = stack_change_prices["roll_essences"]
        case item if item == fossils: roll_cost = stack_change_prices["roll_fossils"]
        case item if item == oils: roll_cost = stack_change_prices["roll_oils"]
        case item if item == scarabs_gilded or item == scarabs_winged: roll_cost = stack_change_prices["roll_scarabs"]
        case item if item == catalysts: roll_cost = stack_change_prices["roll_catalysts"]
    average_profit_per_roll -= average_rolls_to_hit * roll_cost + avg_roll_item_price
    return average_profit_per_roll

def get_profits_of_rerolls():
    profitability = []
    for item_type in all_available_item_types:
        profitability.append("{} - {}".format(item_type[1], round(calculate_average_profit(item_type[0]), 2)))
    print(profitability)

def generate_roll_table(item_type):
    keep_list = get_keep_list(item_type)
    roll_table = PrettyTable(hrules=ALL, padding_width=1)
    roll_table.set_style(SINGLE_BORDER)
    roll_table.field_names = ["", "100% NINJA PRICE", "110% NINJA PRICE", "120% NINJA PRICE", "130% NINJA PRICE", "140% NINJA PRICE", "NINJA PRICE", "BULK PRICE ({}+)".format(BULK_SIZE)]
    for item in item_type:
        current_item = [item]
        for ninja_price_multiplier in range(100, 150, 10):
            current_item.append("Flip profit: {}\nRoll profit: {}".format(format((item_type[item]["bulk_price"] - item_type[item]["price"] * ninja_price_multiplier/100), ".2f"), round(calculate_average_profit(item_type)-item_type[item]["price"], 2)))
        current_item.append(format(item_type[item]["price"], ".2f"))
        current_item.append(format(item_type[item]["bulk_price"], ".2f"))
        roll_table.add_row(current_item)
    print("RE-ROLL UNTIL HIT ANY OF THESE: {}\nAVERAGE CHAOS PROFIT PER RE-ROLL OF A SINGLE ITEM: {} (100% NINJA PRICE)".format(" | ".join(keep_list), round(calculate_average_profit(item_type), 2)))
    print(roll_table)