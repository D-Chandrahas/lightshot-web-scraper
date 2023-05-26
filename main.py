import requests
import random
import string
import re
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import cv2


IMG_URL_REGEX = re.compile(r'<meta property="og:image" content="(.*?)"/>')


def get_img_url(ls_res):
    img_url = IMG_URL_REGEX.search(ls_res.text)
    return None if img_url is None else img_url.group(1)

def filter_img_url(img_url):
    if img_url is None : return None
    if img_url == "//st.prntscr.com/2023/05/26/0610/img/0_173a7b_211be8ff.png" : return None
    if img_url.startswith("https://image.prntscr.com") : return None
    return img_url

i = 0

while True:

    ls_url = "https://prnt.sc/" + ''.join(random.choices(string.digits + string.ascii_lowercase, k=6))
    # ls_url = "https://prnt.sc/" + f'{i}'

    ls_res = requests.get(ls_url,  headers={"Accept": "*/*", "User-Agent": "Python 3"})
    i += 1

    img_url = filter_img_url(get_img_url(ls_res))
    # print(ls_url, img_url)
    # continue

    if img_url is None: continue

    img_host_res = requests.get(img_url, stream=True)
    if img_host_res.status_code == 200:
        print(i, img_url)
        img = Image.open(img_host_res.raw)
        # img.show()

        # plt.imshow(img)
        # plt.show()

        cv2.imshow('image', cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR))
        cv2.waitKey(2000)



        

    


