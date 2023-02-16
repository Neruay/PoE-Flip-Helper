import requests
import json
import time
import cv2
import pytesseract
import numpy as np
from spellchecker import SpellChecker
import io
import PIL
import matplotlib


CHANNEL_ID = 882251982830731315
CHANNEL_ID_2 = 1075437230472048643
AUTHORIZATION_TOKEN = "MjQ5MjQzNzE5MTQ3MDYxMjQ5.Ya5Wsw.G6cHQFDEmiD1Qu5CrPDwbaLDo_4"
item_boxes = [(40, 196), (925, 196), (40, 244), (925, 244), (40, 292), (925, 292), (40, 340), (925, 340), (40, 388), (925, 388), (40, 436), (925, 436), (40, 484), (925, 484), (40, 532), (925, 532), (40, 580), (925, 580), (40, 628), (925, 628)]
item_boxes_alt = [(49, 243), (1154, 243), (49, 303), (1154, 303), (49, 363), (1154, 363), (49, 423), (1154, 423), (49, 483), (1154, 483), (49, 543), (1154, 543), (49, 603), (1154, 603), (49, 663), (1154, 663), (49, 723), (1154, 723), (49, 783), (1154, 783)]
msg_list = []
orb_list = ["fine", "diviners", "skittering", "jewellers", "armoursmiths", "timeless", "fossilised", "imperial", "whispering", "blacksmiths", "amorphous", "foreboding", "obscured", "singular", "thaumaturges", "abyssal", "blighted", "cartographers", "fragmented"]
res = []
def parse_discord_message(msg):
    spell = SpellChecker(language=None, case_sensitive=False)
    spell.word_frequency.load_words(orb_list)
    ninja_multiplier = msg["content"].split(" ")[19][2:-2]
    url = msg["attachments"][0]["url"]
    pytesseract.pytesseract.tesseract_cmd = 'E:/code/Tesseract/tesseract.exe'
    pattern_vector = np.array((32,29,28))
    response = requests.get(url)
    image_bytes = io.BytesIO(response.content)
    img = PIL.Image.open(image_bytes)
    img_full = np.array(img)
    img_full = cv2.cvtColor(img_full, cv2.COLOR_RGB2BGR)
    for i in range(len(item_boxes)):
        cur_x = item_boxes[i][0]
        cur_y = item_boxes[i][1]
        try:
            current_vector = np.array((img_full[cur_y, cur_x][0], img_full[cur_y, cur_x][1], img_full[cur_y, cur_x][2]))
            if np.linalg.norm(pattern_vector - current_vector) < 5:
                roi_amount = img_full[cur_y+12:cur_y + 28, cur_x+13:cur_x + 37] ## 12 28 17 34
                roi_amount = cv2.resize(roi_amount, None, fx=2, fy=2)
                roi_type = img_full[cur_y:cur_y + 38, cur_x + 118:cur_x + 240] # 0 38 118 240
                roi_amount = cv2.cvtColor(roi_amount, cv2.COLOR_BGR2GRAY)
                gray = cv2.cvtColor(roi_type, cv2.COLOR_RGB2GRAY)
                gray, img_bin = cv2.threshold(gray,128,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
                gray = cv2.bitwise_not(img_bin)
                kernel = np.ones((2, 1), np.uint8)
                roi_type = cv2.erode(gray, kernel, iterations=1)
                roi_type = cv2.dilate(roi_type, kernel, iterations=1)

                amount = pytesseract.image_to_string(roi_amount, config='--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789').strip()
                item_type = pytesseract.image_to_string(roi_type, config='--psm 6 --oem 3').strip().lower().replace("’", "")
                if item_type not in orb_list: item_type = spell.correction(item_type)
                res.append((amount, item_type))
        except IndexError:
            break
    print(res)

def get_channel_messages(channelid):
    headers = {"authorization": AUTHORIZATION_TOKEN}
    r = requests.get("https://discord.com/api/v9/channels/{}/messages?limit=7".format(channelid), headers=headers)
    response = json.loads(r.content)
    if response not in msg_list:
        msg_list.clear()
        msg_list.append(response)
        if "Most valuable" in response[6]["content"]:
            parse_discord_message(response[6])
            res = []

while True:
    get_channel_messages(CHANNEL_ID)
    time.sleep(0.1)