from io import BytesIO
import sys
import requests
import random
import string
import re
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import cv2


HEADERS = {
    "User-Agent": "Python 3",
    "Connection": "keep-alive"
}

IMGUR_ERR_IMAGE = requests.get("https://i.imgur.com/removed.png").content

IMG_URL_REGEX = re.compile(r'<img class="no-click screenshot-image" src="(.*?)"')


def random_ls_url(length=6):
    return "https://prnt.sc/" + random.choices("123456789" + string.ascii_lowercase)[0] + "".join(random.choices(string.digits + string.ascii_lowercase, k=length-1))

def get_img_url(ls_res_body):
    img_url = IMG_URL_REGEX.search(ls_res_body)
    return None if img_url is None else img_url.group(1)

def filter_img_url(img_url):
    if img_url is None : return True
    if img_url == "//st.prntscr.com/2023/05/26/0610/img/0_173a7b_211be8ff.png" : return True # use .endswith(0_173a7b_211be8ff.png) or .startswith(//st.prntscr.com)
    # if img_url.startswith("https://image.prntscr.com") : return True
    return False

def filter_img(img):
    if img == IMGUR_ERR_IMAGE : return True
    return False

 
def main():
    print("i, lightshot_url, img_url, img_url_Status , img_host_Status, img_Status")
    i = 0

    while True:

        i += 1
        print(i, end=", ")

        ls_url = random_ls_url()
        print(ls_url, end=", ")

        img_url = get_img_url(requests.get(ls_url,  headers=HEADERS).text)
        print(img_url, end=", ")

        if not filter_img_url(img_url):
            print("img_url_OK", end=", ")

            img_host_res = requests.get(img_url, headers=HEADERS) # type: ignore

            if img_host_res.status_code == 200:
                print("img_Host_200", end=", ")

                enc_img = img_host_res.content
                
                if not filter_img(enc_img):
                    print("img_OK")

                    img = Image.open(BytesIO(enc_img))
                    # img.show()

                    # plt.imshow(img)
                    # plt.show()

                    cv2.imshow('image', cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR))
                    cv2.waitKey(2000)

                else:
                    print("img_Filtered")
            else:
                print(f"img_Host_{img_host_res.status_code}, -")
        else:
            print("img_url_Filtered, -, -")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
