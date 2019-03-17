
from web_runner import download_url
from scan_and_compare import the_differ, scan_output


def main(url):
    download_url(url)


test_url = 'https://packsforcoldbacks.org'


if __name__ == '__main__':
    main(test_url)
    scan_output()
    the_differ()
