from utils import *
from price_info import *
import time

deli_orbs = load_json("deli_orbs.json")

for item in get_ninja_prices("DeliriumOrb").items():
    deli_orbs[item[0]]["price"] = item[1]

quaries = generate_query(deli_orbs.keys())
poetrade_items = []
cnt = 1
for quary in quaries:
    print("Checking {}'s bulk price |{}/{}| Poetrade".format(quary["query"]["type"], cnt, len(quaries)))
    poetrade_items.append(poetrade_query(quary))
    time.sleep(10)
    cnt += 1

for item in poetrade_items:
    deli_orbs[item[0]]["bulk_price"] = item[1]

update_json(deli_orbs, "deli_orbs.json")