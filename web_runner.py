
import requests
from bs4 import BeautifulSoup

from config import OUTPUT_DIR

http_req = 'http://'
https_req = 'https://'
test_url = 'https://joshsisto.com'


def url_checker(url):
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


url_name = url_checker(test_url)

if url_name:
    print('Valid URL. Do something')
    print(f'URL Name: {url_name}')


def download_url(url):
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
    with open(f'{logs_dir}{url_name}__{tstamp}.lnk', 'w') as f:
        for list_item in u_links:
            f.write(f'{list_item}\n')


# url_checker('httpss://joshsisto.com')

