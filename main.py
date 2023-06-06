from io import BytesIO
import requests
import random
import string
import re
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import cv2


IMGUR_ERR_IMAGE = requests.get("https://i.imgur.com/removed.png").content

IMG_URL_REGEX = re.compile(r'<img class="no-click screenshot-image" src="(.*?)"')

def random_ls_url(length=6):
    return "https://prnt.sc/" + random.choices("123456789" + string.ascii_lowercase)[0] + "".join(random.choices(string.digits + string.ascii_lowercase, k=length-1))

def get_img_url(ls_res):
    img_url = IMG_URL_REGEX.search(ls_res.text)
    return None if img_url is None else img_url.group(1)

def filter_img_url(img_url):
    if img_url is None : return True
    if img_url == "//st.prntscr.com/2023/05/26/0610/img/0_173a7b_211be8ff.png" : return True # use .endswith(0_173a7b_211be8ff.png) or .startswith(//st.prntscr.com)
    # if img_url.startswith("https://image.prntscr.com") : return True
    return False


def filter_img(img):
    if img == IMGUR_ERR_IMAGE : return True
    return False
    

i = 0

while True:

    i += 1
    print(i, end=", ")
    ls_url = random_ls_url()
    print(ls_url, end=", ")

    ls_res = requests.get(ls_url,  headers={"Accept": "*/*", "User-Agent": "Python 3"})

    img_url = get_img_url(ls_res)
    print(img_url, end=", ")

    if not filter_img_url(img_url):
        print("url_OK", end=", ")
        img_host_res = requests.get(img_url) # type: ignore
        if img_host_res.status_code == 200:
            print("img_Found", end=", ")
            enc_img = img_host_res.content
            if not filter_img(enc_img):
                print("img_OK")
                # print(i, img_url)
                img = Image.open(BytesIO(enc_img))
                # img.show()

                # plt.imshow(img)
                # plt.show()

                cv2.imshow('image', cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR))
                cv2.waitKey(2000)
            else:
                print("img_Filtered")
        else:
            print("img_Not_Found")
    else:
        print("url_Filtered")


