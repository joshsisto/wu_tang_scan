# old and unused functions


def check_last_scan_2():
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


def check_for_difs(site):
    dif_lst = []
    dif_dir = os.path.join(OUTPUT_DIR, site)
    dif_check = find_files(dif_dir, '*.dif')
    if len(list(dif_check)) > 0:
        # print("Found .dif files")
        for dif in find_files(OUTPUT_DIR, '*.dif'):
            # print(f'Found .dif files {dif}')
            dif_lst.append(dif)
    dif_lst.sort(reverse=True)
    print(f'List of dif files \n {dif_lst}')