
import requests
import filecmp
import time
import datetime
import glob

from bs4 import BeautifulSoup
import smtplib


# while this is true (it is true by default),
def check_site_change():
    # set the url as VentureBeat,
    url = "https://resume.joshsisto.com"
    url_name = url[8:]
    print(url_name)
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')
    print(st)
    # set the headers like we are a browser,
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko)'
                             ' Chrome/72.0.3626.109 Safari/537.36'}
    # download the homepage
    response = requests.get(url, headers=headers)
    # parse the downloaded homepage and grab all text, then,
    # soup = BeautifulSoup(response.text, "lxml")
    # print(response.text)
    # with open(f'{url_name}__{st}.txt', 'w') as f:
    #     print(response.text, file=f)


check_site_change()

# compare = filecmp.cmp("log_1.txt", "log_2.txt", shallow=True)
# print(compare)

prev_scans = glob.glob('*.txt')
# print(prev_scans)

fs_lst = []
for scan_item in prev_scans:
    # print(scan_item)
    split_scan = scan_item.split("__")
    fs_lst.append(split_scan)
    # print(split_scan)

print(fs_lst)

