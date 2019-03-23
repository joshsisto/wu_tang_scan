
import os
import csv
import filecmp
import difflib
from config import (
    OUTPUT_DIR,
    get_platform,
    ensure_dir,
    get_tstamp,
    find_files,
    compare_tstamp
)


platform = get_platform()
if platform == 'OS X' or 'Linux':
    slash = '/'
if platform == 'Windows':
    slash = '\\'


def scan_output():
    """Scan the output directory"""
    print(f'using scan_output() to scan the output directory: {OUTPUT_DIR} for previously scanned sites')
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
        print(f'Scanning directory {s_dir}')
        # get timestamp based on folders
        t_stamp_list = []
        t_stamps = os.listdir(s_dir)
        # create full names to check if they are directories.
        for t_stamp in t_stamps:
            t_path = os.path.join(OUTPUT_DIR, s_dir, t_stamp)
            check_path = os.path.isdir(t_path)
            print(f'Checking path {t_path} {check_path}')
            # if the path exists append the timestamp
            if os.path.isdir(t_path):
                print(f'{t_path} is a dir')
                t_stamp_list.append(t_stamp)
        t_stamp_list.sort(reverse=True)
        # t_stamp_list.append('')
        # compare the timestamps
        t_diff_list = []
        for time_1, time_2 in zip(t_stamp_list[::], t_stamp_list[1::]):
            time_diff = compare_tstamp(time_1, time_2)
            t_diff_list.append(time_diff)
        t_diff_list.append('')
        # find txt files recursively starting at the URL path
        site_list = []
        txt_lst = []
        for txt in find_files(s_dir, '*.txt'):
            # print(f'Found .txt files {txt}')
            txt_lst.append(txt)
            site_list.append(os.path.basename(s_dir))
        txt_lst.sort(reverse=True)
        txt_lst.append('')
        site_list.append('')
        # find html files recursively starting at the URL path
        html_lst = []
        for html in find_files(s_dir, '*.html'):
            # print(f'Found .html files {html}')
            html_lst.append(html)
        html_lst.sort(reverse=True)
        # zip txt and html lists together
        zipper = zip(html_lst, txt_lst, t_stamp_list, t_diff_list, site_list)
        # for item in zipper:
        #     print(f'zipper item {item}')
        # create items.csv file in the root of the scanned site
        with open(f'{s_dir}{slash}scan_index.csv', 'w') as f:
            csv_header = ['html', 'links', 'time_stamp', 'time_difference', 'site', 'comparison']
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
    for s_csv in find_files(OUTPUT_DIR, 'scan_index.csv'):
        print(f'Found scan_index.csv {s_csv}')
        index_csv.append(s_csv)
    # iterate through the csv files scanned and read them
    for si in index_csv:
        # remove empty lines from csv
        remove_empty_lines(si)
        # open newly cleaned file
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
            # log_compare(resp1, resp2)
            # if the log comparison returns false then we are going to run file_diff() against them
            if not log_compare(resp1, resp2):
                # read the html of both files
                text1 = open(resp1, 'r').readlines()
                text2 = open(resp2, 'r').readlines()
                # set variable html_diffs and compare files
                html_diffs = file_diff(text1, text2)
                print(f'{resp1} does not match {resp2}')
                # print('Here are the diffs')
                # print(html_diffs)
                # get the directory of the file to save dif
                dif_dir = os.path.dirname(resp1)
                t_dif = os.path.split(os.path.abspath(resp2))
                t_dif2 = os.path.split(os.path.abspath(t_dif[0]))
                # the 3 lines above this could be done better
                # save dif file using timestamp name of the site it was scanned against
                print(f'saving file {dif_dir}{slash}{t_dif2[1]}.dif')
                print()
                with open(f'{dif_dir}{slash}{t_dif2[1]}.dif', 'w') as f:
                    print(html_diffs, file=f)


def check_last_scan():
    # scan for csv files (currently scan_index) this needs to be updated to only grab scan index
    index_csv = []
    last_scan_list = []
    for s_csv in find_files(OUTPUT_DIR, 'scan_index.csv'):
        # print(f'Found scan_index.csv {s_csv}')
        index_csv.append(s_csv)
    # iterate through the csv files scanned and read them
    for si in index_csv:
        csv_file = open(si)
        reader = csv.reader(csv_file, delimiter=',')
        # append the first row containing the most recent scan
        for ind, row in enumerate(reader):
            if ind == 1:
                last_scan_list.append(row)
            else:
                continue
    print()
    for scan in last_scan_list:
        print(f'Site: {scan[4]} \nLast Scan: {scan[3]} \n')


def check_for_difs():
    dif_lst = []
    dif_check = find_files(OUTPUT_DIR, '*.dif')
    if len(list(dif_check)) > 0:
        print("Found .dif files")
        for dif in find_files(OUTPUT_DIR, '*.dif'):
            print(f'Found .dif files {dif}')
            dif_lst.append(dif)
    dif_lst.sort(reverse=True)
    print(f'List of dif files \n {dif_lst}')


def remove_empty_lines(filename):
    if not os.path.isfile(filename):
        print("{} does not exist ".format(filename))
        return
    with open(filename) as filehandle:
        lines = filehandle.readlines()
    with open(filename, 'w') as filehandle:
        lines = filter(lambda x: x.strip(), lines)
        filehandle.writelines(lines)

