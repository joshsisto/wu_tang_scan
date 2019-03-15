
import os
import requests
from bs4 import BeautifulSoup

from config import (
    OUTPUT_DIR,
    get_platform,
    ensure_dir,
    get_tstamp
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
        # save links as a .lnk file
        with open(f'{URL_TM_DIR_NAME}{slash}links.txt', 'w') as f:
            for list_item in u_links:
                f.write(f'{list_item}\n')

