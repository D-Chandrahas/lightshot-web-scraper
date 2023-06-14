## Introduction

- [prnt.sc](https://prnt.sc/) is a free public image sharing website owned by Skillbrains.
- They also made a screenshot tool called [Lightshot](https://app.prntscr.com/en/index.html) which can be used to take screenshots and upload them to [prnt.sc](https://prnt.sc/).
- Each image is given a unique url which follows the regex `https://prnt.sc/[1-9a-z][0-9a-z]*`
- An image can be uniquely identified by its ID in the latter part of the url.
- The IDs are sequential base 36 numbers (instead of random) and hence images can be mass downloaded by iterating over the IDs.
- This behaviour has been changed and now the IDs are random. However, images uploaded before this change retain their sequential IDs.

## Usage

```
usage: python main.py [-h] [--start_id START_ID] [--length LENGTH] [--count COUNT] [--outdir OUTDIR]

optional arguments:
    -h, --help                           show this help message and exit

    --start_id START_ID, -s START_ID     Start scraping sequentially from START_ID. START_ID should be a alpha-numeric string (Recommended length 6).
                                         If this argument is not given, scraper will scrape random IDs.

    --length LENGTH, -l LENGTH           Length of randomly generted IDs if random scraping is chosen. (Default value is 6).

    --count COUNT, -c COUNT              Scraper will stop after COUNT urls. (Default value is 100).
                        
    --outdir OUTDIR, -o OUTDIR           Path to directory where images will be saved. (Default value is images/).   
```
