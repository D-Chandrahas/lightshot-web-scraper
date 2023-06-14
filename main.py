import os
import random
import re
import string
import sys
from argparse import ArgumentParser
from mimetypes import guess_extension

from numpy import base_repr
import requests



HEADERS = {
    "User-Agent": "Python 3", # change this if cloudflare blocks you
    "Connection": "keep-alive"
}

IMGUR_ERR_IMAGE = requests.get("https://i.imgur.com/removed.png").content

IMG_URL_REGEX = re.compile(r'<img class="no-click screenshot-image" src="(.*?)"')


def get_img_url(ls_res_body):
    img_url = IMG_URL_REGEX.search(ls_res_body)
    return None if img_url == None else img_url.group(1)

def filter_img_url(img_url):
    if img_url == None : return True
    if img_url.startswith("//st.prntscr.com") : return True
    # if img_url.startswith("https://image.prntscr.com") : return True
    return False

def filter_img(img):
    if img == IMGUR_ERR_IMAGE : return True
    return False

def check_args(args):
    if args.start_id != None and not args.start_id.isalnum():
        print("ERROR: start_id should be a alpha-numeric string (Recommended length 6).")
        sys.exit(1)
    if args.length < 1:
        print("ERROR: length should be greater than 0.")
        sys.exit(1)
    if args.count < 1:
        print("ERROR: count should be greater than 0.")
        sys.exit(1)

def random_ls_url(length=6):
    return ("https://prnt.sc/" +
            random.choice("123456789" + string.ascii_lowercase) +
            "".join(random.choices(string.digits + string.ascii_lowercase, k=length-1))
    )

def get_ls_url_from_id10(id10):
    return "https://prnt.sc/" + base_repr(id10, 36).lower()

def save_img(path, img):
    with open(path, "wb") as f:
        f.write(img)

def arguments():
    argparser = ArgumentParser()
    argparser.add_argument("--start_id",
                           "-s",
                           type=str,
                           help="Start scraping sequentially from START_ID. START_ID should be a alpha-numeric string (Recommended length 6). If this argument is not given, scraper will scrape random IDs.")
    argparser.add_argument("--length",
                            "-l",
                            type=int,
                            default=6,
                            help="Length of generted IDs if random scraping is chosen. (Default value is 6).")
    argparser.add_argument("--count",
                            "-c",
                            type=int,
                            default=100,
                            help="Scraper will stop after COUNT urls. (Default value is 100).")
    argparser.add_argument("--outdir",
                            "-o",
                            type=str,
                            default="images/",
                            help="Path to directory where images will be saved. (Default value is images/).")
    return argparser.parse_args()
    
 
def main(args):
    check_args(args)

    os.makedirs(args.outdir, exist_ok=True)

    print("lightshot_url, img_url, img_url_Status , img_host_Status, img_Status")

    id10 = 0 if args.start_id == None else int(args.start_id, 36)

    for _ in range(args.count):

        ls_url = random_ls_url(args.length) if args.start_id == None else get_ls_url_from_id10(id10)
        print(ls_url, end=", ")

        img_url = get_img_url(requests.get(ls_url,  headers=HEADERS).text)
        print(img_url, end=", ")

        if not filter_img_url(img_url):
            print("img_url_OK", end=", ")

            img_host_res = requests.get(img_url, headers=HEADERS) # type: ignore

            if img_host_res.status_code == 200:
                print("img_Host_200", end=", ")

                enc_img = img_host_res.content
                enc_img_extn = guess_extension(img_host_res.headers["Content-Type"])
                if enc_img_extn == None: enc_img_extn = img_url[-4:] # type: ignore
                
                if not filter_img(enc_img):
                    print("img_OK")

                    save_img(os.path.join(args.outdir, ls_url[16:] + enc_img_extn), enc_img)

                else:
                    print("img_Filtered")
            else:
                print(f"img_Host_{img_host_res.status_code}, -")
        else:
            if img_url == None: print("img_url_NotFound, -, -")
            else : print("img_url_Filtered, -, -")

        id10 += 1


if __name__ == "__main__":
    try:
        args = arguments()
        main(args)
    except KeyboardInterrupt:
        sys.exit(0)
