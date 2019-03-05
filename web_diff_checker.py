
import requests
import filecmp
import time
import sys
import datetime
import glob
import pandas as pd
import os
import difflib
from bs4 import BeautifulSoup


def get_platform():
    platforms = {
        'linux1': 'Linux',
        'linux2': 'Linux',
        'darwin': 'OS X',
        'win32': 'Windows'
    }
    if sys.platform not in platforms:
        print(f'Platform: {sys.platform}')
        return sys.platform

    print(f'Platform: {platforms[sys.platform]}')
    return platforms[sys.platform]


platform = get_platform()
if platform == 'OS X' or 'Linux':
    logs_dir = './logs/'
if platform == 'Windows':
    logs_dir = '.\\logs\\'


def ensure_dir(file_path):
    try:
        print(f'checking if {file_path} exists')
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            print(f'directory {file_path} does not exist. Creating...')
            os.makedirs(directory)
    except Exception as x:
        print(f"something fucked up {x}")


# check if the logs directory exists
ensure_dir(logs_dir)


def get_tstamp():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')
    return st


def check_site_change(url):
    """Check url for web changes"""
    # Get url name without https://
    url_name = url[8:]
    print(f'Requesting page {url_name}')
    tstamp = get_tstamp()
    # set the headers like we are a browser
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko)'
                             ' Chrome/72.0.3626.109 Safari/537.36'}
    # download the page
    response = requests.get(url, headers=headers)
    # save downloaded page as a .txt file
    with open(f'{logs_dir}{url_name}__{tstamp}.txt', 'w') as f:
        print(response.text, file=f)


def log_compare(log_1, log_2):
    """compare log_1 and log_2 for differences"""
    compare = filecmp.cmp(log_1, log_2, shallow=True)
    print(compare)
    return compare


def file_diff(text1, text2):
    """compare files for differences"""  # this is currently comparing filenames instead of the files
    diff = difflib.context_diff(text1, text2)
    delta = ''.join(diff)
    print(delta)
    return delta


def check_logs():
    """Check local directory for previous url scans"""
    # create list prev_scans using glob on the local directory
    prev_scans = glob.glob(f'{logs_dir}*.txt')
    txt_lst = []
    # iterate through .txt files and split them if they contain __ (dunder) and append to txt_lst
    for scan_item in prev_scans:
        split_scan = scan_item.split('__')
        txt_lst.append(split_scan)
    log_lst = []
    # trim off the beginning of the web name and remove .txt from timestamp
    for i in txt_lst:
        i[0] = i[0][7:]
        i[1] = i[1][:-4]
        # if there is more than one item in the list append it to log_lst
        if len(i) > 1:
            log_lst.append(i)
    return log_lst


# take the site and time_stamp column and combine them to remake the filename
def txt_sites(site, time_stamp):
    return site + '__' + time_stamp + '.txt'


def main():
    logs = check_logs()
    if len(logs) > 1:
        # data frame column names
        labels = ['site', 'time_stamp']
        # create the dataframe from the logs variable (check_logs())
        df = pd.DataFrame.from_records(logs, columns=labels)
        # create the file_name column by using the txt_sites function with a lambda
        df['file_name'] = df.apply(lambda x: txt_sites(x['site'], x['time_stamp']), axis=1)
        # sort dataframe based off of the file_name column
        df = df.sort_values(['file_name'], ascending=False)
        # reset the index after sorting
        df = df.reset_index(drop=True)
        print(df)
        # iterate through rows of df
        for i in range(1, len(df)):
            # if the sites match compare the files using log_compare()
            if df.site.loc[i-1] == df.site.loc[i]:
                print(f'comparing {logs_dir + df.file_name.loc[i-1]} \n'
                      f'against   {logs_dir + df.file_name.loc[i]} for changes')
                log_compare(logs_dir + df.file_name.loc[i-1], logs_dir + df.file_name.loc[i])
                # if the logs don't match compare them using file_diff()
                if log_compare(logs_dir + df.file_name.loc[i-1], logs_dir + df.file_name.loc[i]) == False:
                    print('Printing differences')
                    text1 = open(logs_dir + df.file_name.loc[i-1], "r").read()
                    text2 = open(logs_dir + df.file_name.loc[i], "r").read()
                    file_diff(text1, text2)


site_2_scan = "https://joshsisto.com"

if __name__ == '__main__':
    # check_site_change(site_2_scan)
    main()

