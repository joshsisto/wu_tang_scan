
import os
import csv
import requests
import difflib
import filecmp
from bs4 import BeautifulSoup

from config import (
    OUTPUT_DIR,
    get_platform,
    ensure_dir,
    get_tstamp,
    find_files
)

http_req = 'http://'
https_req = 'https://'
test_url = 'https://joshsisto.com'

platform = get_platform()
if platform == 'OS X' or 'Linux':
    slash = '/'
if platform == 'Windows':
    slash = '\\'


def url_checker(url):
    """Check if URL starts with http or https"""
    if url.startswith(http_req):
        url_name = url[7:]
        print('http')
        return url_name
    if url.startswith(https_req):
        url_name = url[8:]
        print('https')
        return url_name
    else:
        print('not valid http or https URL')
        return False


def download_url(url):
    """Download URL using requests"""
    # use url_checker to verify URL is using the full address
    url_name = url_checker(url)
    if url_name:
        print(f'Requesting page {url_name}')
        tstamp = get_tstamp()
        # set the headers like we are a browser
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko)'
                                 ' Chrome/72.0.3626.109 Safari/537.36'}
        # download the page
        response = requests.get(url, headers=headers)

        # create directory for saving file
        URL_DIR_NAME = os.path.join(OUTPUT_DIR, str(url_name))
        URL_TM_DIR_NAME = os.path.join(URL_DIR_NAME, str(tstamp))
        # create directory using url name and timestamp for directories
        ensure_dir(URL_TM_DIR_NAME)
        # save downloaded page as a .txt file
        with open(f'{URL_TM_DIR_NAME}{slash}response.html', 'w') as f:
            print(response.text, file=f)
        # use beautiful soup to extract links
        links = []
        soup = BeautifulSoup(response.text, 'html.parser')
        tags = soup.find_all('a')
        # append links to links list
        for tag in tags:
            links.append(tag.get('href'))
        # get only unique values and sort
        my_set = set(links)
        u_links = list(my_set)
        u_links.sort()
        # save links as a .txt file
        with open(f'{URL_TM_DIR_NAME}{slash}links.txt', 'w') as f:
            for list_item in u_links:
                f.write(f'{list_item}\n')


def scan_output():
    """Scan the output directory"""
    print(f'using scan_output() to scan the output directory: \n{OUTPUT_DIR}\n for previously scanned sites')
    # get list of directories in output. These are the sites that have been scanned
    scanned_sites = os.listdir(OUTPUT_DIR)
    # create a list of full path names
    site_dir_lst = []
    for sc_site in scanned_sites:
        # don't get hidden folders
        if not sc_site.startswith('.'):
            site_dir = os.path.join(OUTPUT_DIR, sc_site)
            site_dir_lst.append(site_dir)

    # iterate through list of sites that have been scanned
    for s_dir in site_dir_lst:
        # find txt files recursively starting at the URL path
        txt_lst = []
        for txt in find_files(s_dir, '*.txt'):
            print(f'Found .txt files {txt}')
            txt_lst.append(txt)
        txt_lst.sort()
        # find html files recursively starting at the URL path
        html_lst = []
        for html in find_files(s_dir, '*.html'):
            print(f'Found .html files {html}')
            html_lst.append(html)
        html_lst.sort()
        # zip txt and html lists together
        zipper = zip(html_lst, txt_lst)
        # create items.csv file in the root of the scanned site
        with open(f'{s_dir}{slash}scan_index.csv', 'w') as f:
            csv_header = ['html', 'links', 'comparison']
            writer = csv.writer(f, delimiter=',')
            writer.writerow(csv_header)
            writer.writerows(zipper)


def log_compare(log_1, log_2):
    """compare log_1 and log_2 for differences"""
    compare = filecmp.cmp(log_1, log_2, shallow=True)
    return compare


def file_diff(text1, text2):
    """compare files for differences"""
    diff = difflib.context_diff(text1, text2)
    delta = ''.join(diff)
    return delta


def the_differ():
    """read scan_index.csv first column to compare filenames and return differences"""
    # scan for csv files (currently scan_index) this needs to be updated to only grab scan index
    index_csv = []
    for s_csv in find_files(OUTPUT_DIR, '*.csv'):
        print(f'Found .csv files {s_csv}')
        index_csv.append(s_csv)
    # iterate through the csv files scanned and read them
    for si in index_csv:
        csv_file = open(si)
        reader = csv.reader(csv_file, delimiter=',')
        # save only the first column (html files to be compared)
        resp_list = []
        for row in reader:
            resp_list.append(row[0])
        # remove the first item (this is the index: html)
        resp_list.pop(0)
        # set resp1 and resp2 as filenames to be used for comparison
        for resp1, resp2 in zip(resp_list[::], resp_list[1::]):
            # compare the logs
            log_compare(resp1, resp2)
            # if the log comparison returns false then we are going to run file_diff() against them
            if not log_compare(resp1, resp2):
                # read the html of both files
                text1 = open(resp1, 'r').readlines()
                text2 = open(resp2, 'r').readlines()
                # set variable html_diffs and compare files
                html_diffs = file_diff(text1, text2)
                print(f'{resp1} does not match {resp2}')
                print()
                print('Here are the diffs')
                print(html_diffs)






