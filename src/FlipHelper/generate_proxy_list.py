import requests
import pandas as pd
import warnings
import json
from bs4 import BeautifulSoup

warnings.simplefilter(action='ignore', category=FutureWarning)
url = "https://free-proxy-list.net/"

data = requests.get(url).text
soup = BeautifulSoup(data, 'html.parser')
table = soup.find('table', class_='table table-striped table-bordered')

df = pd.DataFrame(columns=['IP', 'Port', 'Https'])

for row in table.tbody.find_all('tr'):    
    columns = row.find_all('td')
    if(columns != []) and columns[6].text == "yes":
        IP = columns[0].text.strip()
        Port = columns[1].text.strip()
        Country = columns[3].text.strip()
        Https = columns[6].text.strip()
        df = df.append({'IP': IP,  'Port': Port, 'Https': Https}, ignore_index=True)

proxy_list = []

for x in range(10):
    ip_address = df.loc[x, "IP"] + ":" + df.loc[x, "Port"]
    proxy_list.append({"http": ip_address, "https": ip_address})

with open("proxy_list.json", "w") as outfile:
        json.dump(proxy_list, outfile, indent=4)