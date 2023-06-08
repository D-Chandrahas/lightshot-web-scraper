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
from argparse import ArgumentParser


HEADERS = {
    "User-Agent": "Python 3",
    "Connection": "keep-alive"
}

IMGUR_ERR_IMAGE = requests.get("https://i.imgur.com/removed.png").content

IMG_URL_REGEX = re.compile(r'<img class="no-click screenshot-image" src="(.*?)"')


def rand_ls_id36(length=6):
    return (random.choice("123456789" + string.ascii_lowercase) +
            "".join(random.choices(string.digits + string.ascii_lowercase, k=length-1))
    )

def random_ls_url(length=6):
    return "https://prnt.sc/" + rand_ls_id36(length)

def get_ls_url_from_id10(id10):
    return "https://prnt.sc/" + np.base_repr(id10, 36)

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

def arguments():
    argparser = ArgumentParser()
    argparser.add_argument("--start_id",
                           "-s",
                           type=str,
                           help="Start scraping sequentially from this lightshot id. id should be a alpha-numeric string of length 6/7. If this arg is not given, scrape random ids")
    argparser.add_argument("--length",
                            "-l",
                            type=int,
                            default=6,
                            help="Length of lightshot id for random scraping. Default value is 6.")
    argparser.add_argument("--count",
                            "-c",
                            type=int,
                            default=100,
                            help="Scraper will stop after this many images. Default value is 100.")
    argparser.add_argument("--outdir",
                            "-o",
                            type=str,
                            default="images/",
                            help="Path to directory where images will be saved. Default value is images/.")
    return argparser.parse_args()
    
 
def main(args):
    print("lightshot_url, img_url, img_url_Status , img_host_Status, img_Status")
    id10 = 0 if args.start_id == False else int(args.start_id, 36)

    for _ in range(args.count):

        ls_url = random_ls_url(args.length) if args.start_id == False else get_ls_url_from_id10(id10)
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

        id10 += 1

if __name__ == "__main__":
    try:
        args = arguments()
        main(args)
    except KeyboardInterrupt:
        sys.exit(0)
