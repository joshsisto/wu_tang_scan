
import requests
import filecmp
import time
import sys
import datetime
import glob
import pandas as pd
from bs4 import BeautifulSoup


def get_platform():
    platforms = {
        'linux1': 'Linux',
        'linux2': 'Linux',
        'darwin': 'OS X',
        'win32': 'Windows'
    }
    if sys.platform not in platforms:
        return sys.platform

    return platforms[sys.platform]


platform = get_platform()
print(f"Platform:{platform}")
if platform == 'OS X' or 'Linux':
    logs_dir = './logs/'
if platform == 'Windows':
    logs_dir = '.\\logs\\'


def get_tstamp():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')
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
    # save downloaded page as a .txt file
    with open(f'{logs_dir}{url_name}__{tstamp}.txt', 'w') as f:
        print(response.text, file=f)


check_site_change()

# compare = filecmp.cmp("log_1.txt", "log_2.txt", shallow=True)
# print(compare)

def check_logs():
    """Check local directory for previous url scans"""
    # create list prev_scans using glob on the local directory
    prev_scans = glob.glob('./logs/*.txt')
    txt_lst = []
    # iterate through .txt files and split them if they contain __ (dunder) and append to fs_lst
    for scan_item in prev_scans:
        split_scan = scan_item.split("__")
        txt_lst.append(split_scan)
    log_lst = []
    # trim off the beginning of the web name and remove .txt from timestamp
    for i in txt_lst:
        i[0] = i[0][7:]
        i[1] = i[1][:-4]
        # if there is more than one item in the list append it to f_lst
        if len(i) > 1:
            log_lst.append(i)
    return log_lst


logs = check_logs()


# take the site and time_stamp column and combine them to remake the filename
def txt_sites(site, time_stamp):
    return site + "__" + time_stamp + ".txt"


# data frame column names
labels = ['site', 'time_stamp']
# create the dataframe from the logs variable (check_logs())
df = pd.DataFrame.from_records(logs, columns=labels)
# create the file_name column by using the txt_sites function with a lambda
df['file_name'] = df.apply(lambda x: txt_sites(x['site'], x['time_stamp']), axis=1)
# create a new variable df_sort and sort the original dataframe based off of the file_name column
df_sort = df.sort_values(["file_name"], ascending=False)
print(df_sort)



