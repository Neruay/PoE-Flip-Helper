import requests
import json
import time
import cv2
import pytesseract
import numpy as np
import io
import PIL
import matplotlib
from settings import *
from spellchecker import SpellChecker

msg_list = []
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
    for i in range(len(ITEM_BOXES)):
        cur_x = ITEM_BOXES[i][0]
        cur_y = ITEM_BOXES[i][1]
        try:
            current_vector = np.array((img_full[cur_y, cur_x][0], img_full[cur_y, cur_x][1], img_full[cur_y, cur_x][2]))
            if np.linalg.norm(pattern_vector - current_vector) < 5:
                roi_amount = img_full[cur_y+12:cur_y + 28, cur_x+13:cur_x + 37]
                roi_amount = cv2.resize(roi_amount, None, fx=2, fy=2)
                roi_type = img_full[cur_y:cur_y + 38, cur_x + 118:cur_x + 240]
                roi_amount = cv2.cvtColor(roi_amount, cv2.COLOR_BGR2GRAY)
                gray = cv2.cvtColor(roi_type, cv2.COLOR_RGB2GRAY)
                gray, img_bin = cv2.threshold(gray,128,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
                gray = cv2.bitwise_not(img_bin)
                kernel = np.ones((2, 1), np.uint8)
                roi_type = cv2.erode(gray, kernel, iterations=1)
                roi_type = cv2.dilate(roi_type, kernel, iterations=1)

                amount = pytesseract.image_to_string(roi_amount, config='--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789').strip()
                item_type = pytesseract.image_to_string(roi_type, config='--psm 6 --oem 3').strip().lower().replace("’", "")
                if item_type not in ORB_LIST: item_type = spell.correction(item_type)
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