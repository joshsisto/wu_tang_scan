#!/usr/bin/env python3

import sys
from web_runner import download_url, url_checker
from scan_and_compare import the_differ, scan_output, check_last_scan, recent_change


__AUTHOR__ = 'Josh Sisto <joshsisto@gmail.com>'
__VERSION__ = 'v0.01'
__DESCRIPTION__ = 'wdc usage:  Scan website for changes'
__DOCUMENTATION__ = 'https://github.com/llamafarmer/wu_tang_scan'
__EXAMPLE__ = './run_wdc https://joshsisto.com'


def wdc_help():
    print('No argument given for site to check')
    print(__DESCRIPTION__)
    print(f'Documentation: {__DOCUMENTATION__}')
    print(f'Example usage: {__EXAMPLE__}')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        test_url = sys.argv[1]
        site = url_checker(test_url)
        download_url(test_url)
        scan_output()
        the_differ()
        check_last_scan(site)
        recent_change(site)
    else:
        wdc_help()
