
import requests
import filecmp
import time
import datetime
import glob
from bs4 import BeautifulSoup


def get_tstamp():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')
    return st


def check_site_change():
    """Check url for web changes"""
    # Get url and url name
    url = "https://joshsisto.com"
    url_name = url[8:]
    print(f'Requesting page {url_name}')
    tstamp = get_tstamp()
    # set the headers like we are a browser,
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko)'
                             ' Chrome/72.0.3626.109 Safari/537.36'}
    # download the page
    response = requests.get(url, headers=headers)
    with open(f'{url_name}__{tstamp}.txt', 'w') as f:
        print(response.text, file=f)


check_site_change()

# compare = filecmp.cmp("log_1.txt", "log_2.txt", shallow=True)
# print(compare)


def check_logs():
    """Check local directory for previous url scans"""
    # create list prev_scans using glob on the local directory
    prev_scans = glob.glob('*.txt')
    fs_lst = []
    for scan_item in prev_scans:
        split_scan = scan_item.split("__")
        fs_lst.append(split_scan)
    f_lst = []
    for i in fs_lst:
        if len(i) > 1:
            f_lst.append(i)
    return f_lst


something = check_logs()
print(something)

