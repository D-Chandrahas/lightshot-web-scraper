import requests
import random
import string
import re
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import cv2


i = 0

while True:

    reqUrl = "https://prnt.sc/" + ''.join(random.choices(string.digits + string.ascii_lowercase, k=6))

    ls_res = requests.get(reqUrl,  headers={"Accept": "*/*", "User-Agent": "Python 3"})
    i += 1
    # img_url = ls_res.text.split("<meta property=\"og:image\" content=\"")[1].split("\"")[0]
    # print(img_url)

    img_url = re.search(r"https://i\.imgur\.com/[a-zA-Z0-9]{7}\.(png|jpg|jpeg)", ls_res.text)

    if img_url is None:
        continue
        img_url = re.search(r"https://image\.prntscr\.com/image/([a-zA-Z0-9_\-]{22}|[a-zA-Z0-9_\-]{32})\.(png|jpg|jpeg)", ls_res.text)

        if img_url is None:
            continue

    img_url = img_url.group()

    img_host_res = requests.get(img_url, stream=True)
    if img_host_res.status_code == 200:
        print(i, img_url)
        img = Image.open(img_host_res.raw)
        # img.show()

        # plt.imshow(img)
        # plt.show()

        cv2.imshow('image', cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR))
        cv2.waitKey(2000)



        

    


