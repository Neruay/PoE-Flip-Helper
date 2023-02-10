import requests
import json
import os
from settings import POE_SESSION_ID, USER_AGENT, LEAGUE

__CURRENT_DIR__, _ = os.path.split(__file__)
__CURRENT_PATH__ = os.path.join(__CURRENT_DIR__, "")
__PRICES_PATH__ = os.path.join(__CURRENT_PATH__, "price_info")

def load_json(json_file_path: str, base_path=__PRICES_PATH__):
    file_path = os.path.join(base_path, json_file_path)
    with open(file_path) as json_data:
        try:
            return json.load(json_data)
        except json.decoder.JSONDecodeError:
            print(f"Warning: {json_file_path} failed to decode json")

def update_json(data: dict, json_file: str, base_path=__PRICES_PATH__):
    path = os.path.join(__PRICES_PATH__, json_file)
    with open(path, "w") as outfile:
        json.dump(data, outfile, indent=4)

def get_ninja_prices(item_type: str) -> dict:
    prices = {}
    ninja_url_template = "https://poe.ninja/api/data/itemoverview?league={}&type={}&language=en".format(LEAGUE, item_type)
    response = json.loads(requests.get(ninja_url_template).content)
    for item in response["lines"]:
        prices[item["name"]] = round(item["chaosValue"], 1)
    return prices

def generate_query(item_list: list, stacksize=10) -> list:
    query_list = []
    for item in item_list:
        query_list.append({"query":{"status":{"option":"online"},"type":item,"stats":[{"type":"and","filters":[]}],"filters":{"misc_filters":{"filters":{"stack_size":{"min":stacksize}}}}},"sort":{"price":"asc"}})
    return query_list

def poetrade_query(query: str, proxy: dict) -> tuple:
    trade_url = "https://www.pathofexile.com/api/trade/search/Sanctum"
    headers = {"POESESSID": POE_SESSION_ID, "user-agent": USER_AGENT}
    response = requests.post(trade_url, headers=headers, json=query, proxies=proxy)
    parsed = json.loads(response.content)

    query_id = parsed["id"]
    items = parsed["result"]
    item_id_list = ""
    items = items[:10]
    for item in items:
        item_id_list += item + ","
    item_id_list = item_id_list[:-1]
    fetched_items = requests.get("https://www.pathofexile.com/api/trade/fetch/{}?query={}".format(item_id_list, query_id), headers=headers, proxies=proxy)
    parsed_items = json.loads(fetched_items.content)
    parsed_items = parsed_items["result"]
    prices = []

    for item in parsed_items:
        prices.append(item["listing"]["price"]["amount"])
    median = sum(prices)/len(prices)
    if median/prices[0] >= 1.2:
        prices = prices[1:]
        median = sum(prices)/len(prices)
    return (parsed_items[0]["item"]["baseType"], round(median, 1), prices)